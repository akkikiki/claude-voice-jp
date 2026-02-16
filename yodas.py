import io
import json
import random
import tarfile

import sounddevice as sd
import soundfile as sf
from huggingface_hub import hf_hub_download

REPO_ID = "espnet/yodas2"
LANG = "ja000"
SHARD = random.randint(0, 5)  # pick a random shard

shard_id = f"{SHARD:08d}"
print(f"Downloading shard {shard_id} for {LANG}...")

audio_tar_path = hf_hub_download(repo_id=REPO_ID, filename=f"data/{LANG}/audio/{shard_id}.tar.gz", repo_type="dataset")
text_path = hf_hub_download(repo_id=REPO_ID, filename=f"data/{LANG}/text/{shard_id}.json", repo_type="dataset")
duration_path = hf_hub_download(repo_id=REPO_ID, filename=f"data/{LANG}/duration/{shard_id}.txt", repo_type="dataset")

# Load text metadata
with open(text_path, "r") as f:
    json_obj_lst = json.load(f)

video2text = {}
for obj in json_obj_lst:
    video_id = obj["audio_id"]
    utts = []
    for k, v in sorted(obj["text"].items()):
        fields = k.split("-")
        start = float(fields[-2]) / 100
        end = float(fields[-1]) / 100
        utts.append({"utt_id": k, "text": v, "start": start, "end": end})
    video2text[video_id] = utts

# Load duration metadata
video2duration = {}
with open(duration_path) as f:
    for row in f:
        fields = row.strip().split()
        video2duration[fields[0]] = float(fields[1])

# Build index of audio members, shuffle, then play randomly
print(f"Indexing audio from shard {shard_id}...")
with tarfile.open(audio_tar_path, "r:gz") as tar:
    members = [m for m in tar.getmembers() if m.isfile() and m.name.rsplit("/", 1)[-1].rsplit(".", 1)[0] in video2text]

random.shuffle(members)
print(f"Found {len(members)} samples. Playing in random order...\n")

with tarfile.open(audio_tar_path, "r:gz") as tar:
    for i, member in enumerate(members):
        video_id = member.name.rsplit("/", 1)[-1].rsplit(".", 1)[0]

        audio_bytes = tar.extractfile(member).read()
        data, sr = sf.read(io.BytesIO(audio_bytes))

        duration = video2duration.get(video_id, len(data) / sr)
        utts = video2text[video_id]
        print(f"[{i}] video_id={video_id}  duration={duration:.1f}s  sr={sr}")
        for u in utts:
            print(f"    [{u['start']:.1f}-{u['end']:.1f}] {u['text']}")

        sd.play(data, samplerate=sr)
        sd.wait()

        choice = input("Press Enter for next, q to quit: ")
        if choice.strip().lower() == "q":
            break
