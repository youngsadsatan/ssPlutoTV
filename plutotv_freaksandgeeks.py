# plutotv_freaksandgeeks.py

import uuid
import os

# Dados dos episódios fornecidos manualmente
EPISODES = [
    { "season": 1, "episode": 1,  "title": "Piloto",                                "episode_id": "60959ee4d9b0ce0014e4b694" },
    { "season": 1, "episode": 2,  "title": "Cervejas e Açudes",                     "episode_id": "60959e2141fc48001326c5af" },
    { "season": 1, "episode": 3,  "title": "Truques e Travessuras",                "episode_id": "60959e2341fc48001326c5d6" },
    { "season": 1, "episode": 4,  "title": "Kim Kelley é Minha Amiga",             "episode_id": "60959e2141fc48001326c59a" },
    { "season": 1, "episode": 5,  "title": "Testes e Seios",                        "episode_id": "60959e2041fc48001326c553" },
    { "season": 1, "episode": 6,  "title": "Eu Estou Com a Banda",                   "episode_id": "60959e2541fc48001326c674" },
    { "season": 1, "episode": 7,  "title": "Cardado e Descartado",                   "episode_id": "60959e2e41fc48001326c6f2" },
    { "season": 1, "episode": 8,  "title": "Namoradas e Namorados",                  "episode_id": "60959e2541fc48001326c65d" },
    { "season": 1, "episode": 9,  "title": "Temos Espírito",                         "episode_id": "60959e2641fc48001326c689" },
    { "season": 1, "episode": 10, "title": "O Diário",                               "episode_id": "60959e2341fc48001326c615" },
    { "season": 1, "episode": 11, "title": "Aparência e Livros",                     "episode_id": "60959e2141fc48001326c585" },
    { "season": 1, "episode": 12, "title": "A Porta da Garagem",                    "episode_id": "60959e2641fc48001326c6a7" },
    { "season": 1, "episode": 13, "title": "Engasgando e Fumando",                  "episode_id": "60959e2341fc48001326c5eb" },
    { "season": 1, "episode": 14, "title": "Cachorros Mortos e Professores de Ginástica", "episode_id": "60959e2e41fc48001326c707" },
    { "season": 1, "episode": 15, "title": "Noshing e Moshing",                     "episode_id": "60959f4c72e8e300148a367f" },
    { "season": 1, "episode": 16, "title": "Beijar e Vagabundear",                  "episode_id": "60959e2341fc48001326c62b" },
    { "season": 1, "episode": 17, "title": "As Pequenas Coisas",                    "episode_id": "60959e2341fc48001326c600" },
    { "season": 1, "episode": 18, "title": "Discotecas e Dragões",                   "episode_id": "60959e2141fc48001326c56e" },
]

def generate_hls_url(episode_id):
    """Gera URL HLS válida para o episódio"""
    sid = str(uuid.uuid4())
    device_id = f"web_{str(uuid.uuid4())[:8]}"
    return (
        f"https://service-stitcher.clusters.pluto.tv/stitch/hls/episode/{episode_id}/master.m3u8?"
        f"deviceType=web&deviceMake=Chrome&deviceModel=Chrome&sid={sid}&deviceId={device_id}&"
        "deviceVersion=unknown&appVersion=unknown&deviceDNT=0&userId=&advertisingId=&"
        "deviceLat=&deviceLon=&app_name=web&appName=web&buildVersion=&deviceCategory=web&"
        "app_device=web&marketingRegion=BR"
    )

def generate_m3u_playlist():
    m3u_content = "#EXTM3U\n"

    for ep in EPISODES:
        season_str = str(ep["season"]).zfill(2)
        episode_str = str(ep["episode"]).zfill(2)
        tvg_id = f"FreaksGeeks.S{season_str}E{episode_str}"
        hls_url = generate_hls_url(ep["episode_id"])

        m3u_content += (
            f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{ep["title"]}" '
            f'group-title="Freaks and Geeks", S{season_str}E{episode_str} • {ep["title"]}\n'
        )
        m3u_content += f"{hls_url}\n\n"

    # garante que pasta de saída exista
    os.makedirs('output', exist_ok=True)
    # salva o arquivo
    out_path = os.path.join('output', 'freaks_and_geeks.m3u')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(m3u_content)
    print(f'Playlist gerada em {out_path}')

if __name__ == "__main__":
    generate_m3u_playlist()
