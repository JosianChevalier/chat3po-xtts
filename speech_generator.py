import os
from dataclasses import dataclass

from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from torch import Tensor
import torch
import torchaudio

from config import Chat3POSpeechConfig, Model


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
            speed=speed, # Speed of the speech
            repetition_penalty=2.0,
        )

        torchaudio.save(output_file_path, torch.tensor(out["wav"]).unsqueeze(0), 24000)

def load_model(config: Chat3POSpeechConfig):
    model = load_xtts_model(config)

    print("Computing speaker latents...")
    conditional_latent, speaker_embedding = model.get_conditioning_latents(audio_path=config.speaker_reference)

    return SpeechGenerator(
        model=model,
        conditional_latent=conditional_latent,
        speaker_embedding=speaker_embedding,
    )

@dataclass
class ModelConfig:
    xtts_config_path: str
    xtts_vocab_file: str
    xtts_model: str
    speaker_file_path: str


def model_files_from(model: Model):
    local_folder = os.path.expanduser("~/.local")

    if model == Model.CUSTOM_C3PO:
        return ModelConfig(
            xtts_config_path="./model/config.json",
            xtts_vocab_file = "./model/vocab.json",
            xtts_model = "./model/model.pth",
            speaker_file_path=f"{local_folder}/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/speakers_xtts.pth",
        )
    elif model == Model.XTTS_V2:
        return ModelConfig(
            xtts_config_path=f"{local_folder}/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/config.json",
            xtts_vocab_file=f"{local_folder}/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/vocab.json",
            xtts_model=f"{local_folder}/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/model.pth",
            speaker_file_path=f"{local_folder}/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/speakers_xtts.pth",
        )
    else:
        print("Unknown model:", model)

def load_xtts_model(config: Chat3POSpeechConfig):
    print(f"Loading model {config.model.value}...")
    model_files = model_files_from(config.model)

    xtts_config = XttsConfig()
    xtts_config.load_json(model_files.xtts_config_path)
    model = Xtts.init_from_config(xtts_config)
    model.load_checkpoint(
        xtts_config,
        checkpoint_path=model_files.xtts_model,
        vocab_path=model_files.xtts_vocab_file,
        use_deepspeed=False,
        speaker_file_path=model_files.speaker_file_path,
    )

    if config.use_cuda:
        model.cuda()

    return model
