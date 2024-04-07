from dataclasses import dataclass

from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from torch import Tensor
import torch
import torchaudio

from config import Chat3POSpeechConfig

@dataclass
class SpeechGenerator:
    model: Xtts
    conditional_latent: Tensor
    speaker_embedding: Tensor

    def generate(self, sentence: str, output_file_path: str, temperature: float, speed: float):
        out = self.model.inference(
            sentence,
            "fr",
            self.conditional_latent,
            self.speaker_embedding,
            temperature=temperature, # Variability of the output. The higher, the more variable
            speed=speed # Speed of the speech
        )

        torchaudio.save(output_file_path, torch.tensor(out["wav"]).unsqueeze(0), 24000)

def load_model(config: Chat3POSpeechConfig):
    print("Loading model...")

    model = load_xtts_model(config)

    print("Computing speaker latents...")
    conditional_latent, speaker_embedding = model.get_conditioning_latents(audio_path=config.speaker_reference)

    return SpeechGenerator(
        model=model,
        conditional_latent=conditional_latent,
        speaker_embedding=speaker_embedding,
    )


def load_xtts_model(config: Chat3POSpeechConfig):
    xtts_config_path="./model/config.json"
    xtts_vocab_file="./model/vocab.json"
    xtts_model="./model/model.pth"
    speaker_file_path = "recipes/ljspeech/xtts_v1/run/training/GPT_XTTS_LJSpeech_FT/speakers_xtts.pth",

    xtts_config = XttsConfig()
    xtts_config.load_json(xtts_config_path)
    model = Xtts.init_from_config(xtts_config)
    model.load_checkpoint(
        xtts_config,
        checkpoint_path=xtts_model,
        vocab_path=xtts_vocab_file,
        use_deepspeed=False,
        speaker_file_path=speaker_file_path,
    )

    if config.use_cuda:
        model.cuda()

    return model
