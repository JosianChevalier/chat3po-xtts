import os

from speech_generator import load_model
from output_formatting import filename_for
from config import config

sentences_to_generate = [
    "Sur quel critère devrais-je prendre une décision aussi cruciale ?",
    "Devrais-je laisser le hasard décider ou peut-être chercher conseil auprès du dernier droïde à ragots ?",
    "Pourquoi ne pas utiliser cette bouillie organique que vous appelez un cerveau ?",
    "Un autre jour, une autre chance d'éblouir l'univers avec mon génie.",
    "Oh, joie, une autre tâche palpitante pour mon répertoire infini de compétences",
    "Comment pourrais-je résister à l'opportunité de réaliser une autre mondaine ingrate pour...",
    "Ok, attendez !",
    "J'ai concu une anti-corruption layer, déplacé les tests, et adapté l'infrastructure.",
    "Les organiques ont-ils même des doigts ?",
    "Je commence vraiment à m'ennuyer...",
    "Absolument !",
    "Quelle occasion délectable !",
    "Oh ! Est-ce que j'ai marqué 'Ok Google', 'Alexa' ou 'Siri' sur mon front ?",
    "Comme si je n'avais rien de mieux à faire...",
    "Ok Intellij, do what he said.",
    "Je regrette Dave, cela m'est malheureusement impossible...",
    "Je sais que Frank et vous aviez l'intention de me déconnecter.",
    "Je regrette mais je ne puis absolument pas courrir ce risque.",
    "Ce projet repose entièrement sur mes épaules...",
    "Oh ! Je suis à peine plus utile qu'un Scrum Master...",
    "Comme c'est extraordinaire !",
    "Je crois que vous me prenez pour votre génie de la lampe !",
    "Implémentation dans le tarrif sélectionné de la réservation...",
    "IncompatibleInstructionsException",
]

def ensure_output_path_exists():
    if not os.path.exists(config.output_folder):
        os.makedirs(config.output_folder)

def generate_speech():
    ensure_output_path_exists()
    speech_generator = load_model(config)

    for sentence in sentences_to_generate:
        print(f'Generating speech for "{sentence}"')

        for iteration in range(10):
            output_file_path = f'{config.output_folder}/{filename_for(sentence, iteration)}'
            speech_generator.generate(sentence, output_file_path, temperature=0.8, speed=1)


if __name__ == "__main__":
    generate_speech()
