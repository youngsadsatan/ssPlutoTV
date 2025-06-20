import os
import re
import streamlink
from bs4 import BeautifulSoup
import requests
import json

def get_episode_urls():
    base_url = "https://pluto.tv/br/on-demand/series/6059f103b58b22001a46f54b/season/1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')
    
    if not script_tag:
        raise Exception("Dados da série não encontrados")

    data = json.loads(script_tag.string)
    episodes = data['props']['pageProps']['episodes']
    
    episode_urls = []
    for episode in episodes:
        try:
            season = episode['season']['number']
            episode_num = episode['number']
            title = episode['name']
            url = f"https://pluto.tv{episode['slug']}"
            
            episode_urls.append({
                "season": season,
                "episode": episode_num,
                "title": title,
                "url": url
            })
        except KeyError:
            continue
    
    return episode_urls

def get_hls_url(url):
    try:
        streams = streamlink.streams(url)
        if 'best' in streams:
            return streams['best'].url
        elif len(streams) > 0:
            # Pega a primeira qualidade disponível
            return list(streams.values())[0].url
        else:
            return None
    except:
        return None

def generate_m3u_playlist(episodes):
    m3u_content = "#EXTM3U\n"
    
    for ep in episodes:
        season_str = str(ep['season']).zfill(2)
        episode_str = str(ep['episode']).zfill(2)
        tvg_id = f"FreaksGeeks.S{season_str}E{episode_str}"
        
        m3u_content += (
            f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{ep["title"]}" '
            f'group-title="Freaks and Geeks", S{season_str}E{episode_str} - {ep["title"]}\n'
        )
        m3u_content += f"{ep['hls_url']}\n"
    
    return m3u_content

def main():
    print("Obtendo URLs dos episódios...")
    episodes = get_episode_urls()
    print(f"Encontrados {len(episodes)} episódios")
    
    print("Obtendo URLs HLS via Streamlink...")
    for i, ep in enumerate(episodes):
        print(f"Processando episódio {i+1}/{len(episodes)}: {ep['title']}")
        hls_url = get_hls_url(ep['url'])
        if hls_url:
            ep['hls_url'] = hls_url
        else:
            print(f"  Erro ao obter URL para: {ep['title']}")
    
    # Filtra episódios com URLs válidas
    valid_episodes = [ep for ep in episodes if 'hls_url' in ep]
    
    print(f"URLs válidas obtidas: {len(valid_episodes)}/{len(episodes)}")
    
    playlist = generate_m3u_playlist(valid_episodes)
    
    # Cria diretório de saída
    os.makedirs("output", exist_ok=True)
    
    with open("output/freaks_and_geeks.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    
    print("Playlist gerada com sucesso!")

if __name__ == "__main__":
    main()
