import requests
import re
import uuid
from bs4 import BeautifulSoup
import json

def get_episode_data():
    base_url = "https://pluto.tv/br/on-demand/series/6059f103b58b22001a46f54b/season/1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    session = requests.Session()
    response = session.get(base_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar a página: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')
    
    if not script_tag:
        raise Exception("Dados da série não encontrados")

    data = json.loads(script_tag.string)
    episodes = data['props']['pageProps']['episodes']
    
    if not episodes:
        raise Exception("Nenhum episódio encontrado")

    episode_list = []
    for episode in episodes:
        try:
            season = episode['season']['number']
            episode_num = episode['number']
            title = episode['name']
            episode_id = episode['_id']
            
            # Gera UUID para parâmetros da URL
            sid = str(uuid.uuid4())
            device_id = f"web_{str(uuid.uuid4())[:8]}"
            
            # Constrói URL HLS
            hls_url = (
                f"https://service-stitcher.clusters.pluto.tv/stitch/hls/episode/{episode_id}/master.m3u8?"
                f"deviceType=web&deviceMake=Chrome&deviceModel=Chrome&sid={sid}&deviceId={device_id}&"
                "deviceVersion=unknown&appVersion=unknown&deviceDNT=0&userId=&advertisingId=&"
                "deviceLat=&deviceLon=&app_name=web&appName=web&buildVersion=&deviceCategory=web&"
                "app_device=web&marketingRegion=BR"
            )
            
            episode_list.append({
                "season": season,
                "episode": episode_num,
                "title": title,
                "url": hls_url
            })
        except KeyError as e:
            print(f"Erro ao processar episódio: {e}")
            continue
    
    return episode_list

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
        m3u_content += f"{ep['url']}\n\n"
    
    return m3u_content

def main():
    try:
        episodes = get_episode_data()
        playlist = generate_m3u_playlist(episodes)
        
        with open("freaks_and_geeks.m3u", "w", encoding="utf-8") as f:
            f.write(playlist)
        
        print("Playlist gerada com sucesso!")
    
    except Exception as e:
        print(f"Erro no processo principal: {str(e)}")
        raise

if __name__ == "__main__":
    main()
