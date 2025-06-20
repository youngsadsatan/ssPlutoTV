# plutotv_freaksandgeeks.py

import uuid
import os

# Manual list of episodes
EPISODES = [
    {"season": 1, "episode": 1,  "title": "Pilot",                               "episode_id": "60959ee4d9b0ce0014e4b694"},
    {"season": 1, "episode": 2,  "title": "Beers and Ponds",                     "episode_id": "60959e2141fc48001326c5af"},
    {"season": 1, "episode": 3,  "title": "Pranks and Tricks",                   "episode_id": "60959e2341fc48001326c5d6"},
    {"season": 1, "episode": 4,  "title": "Kim Kelly Is My Friend",             "episode_id": "60959e2141fc48001326c59a"},
    {"season": 1, "episode": 5,  "title": "Tests and Tits",                      "episode_id": "60959e2041fc48001326c553"},
    {"season": 1, "episode": 6,  "title": "I'm in a Band",                      "episode_id": "60959e2541fc48001326c674"},
    {"season": 1, "episode": 7,  "title": "Carded and Discarded",               "episode_id": "60959e2e41fc48001326c6f2"},
    {"season": 1, "episode": 8,  "title": "Girlfriends and Boyfriends",          "episode_id": "60959e2541fc48001326c65d"},
    {"season": 1, "episode": 9,  "title": "We Have Spirit",                      "episode_id": "60959e2641fc48001326c689"},
    {"season": 1, "episode": 10, "title": "The Diary",                          "episode_id": "60959e2341fc48001326c615"},
    {"season": 1, "episode": 11, "title": "Appearance and Books",               "episode_id": "60959e2141fc48001326c585"},
    {"season": 1, "episode": 12, "title": "The Garage Door",                    "episode_id": "60959e2641fc48001326c6a7"},
    {"season": 1, "episode": 13, "title": "Choking and Smoking",                "episode_id": "60959e2341fc48001326c5eb"},
    {"season": 1, "episode": 14, "title": "Dead Dogs and Gym Teachers",         "episode_id": "60959e2e41fc48001326c707"},
    {"season": 1, "episode": 15, "title": "Noshing and Moshing",                "episode_id": "60959f4c72e8e300148a367f"},
    {"season": 1, "episode": 16, "title": "Kissing and Loafing",                "episode_id": "60959e2341fc48001326c62b"},
    {"season": 1, "episode": 17, "title": "The Little Things",                 "episode_id": "60959e2341fc48001326c600"},
    {"season": 1, "episode": 18, "title": "Discos and Dragons",                "episode_id": "60959e2141fc48001326c56e"},
]

def generate_hls_url(episode_id):
    """Generate a master HLS URL for an episode"""
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
    """Create M3U playlist pointing to master HLS URLs"""
    m3u = ["#EXTM3U"]

    for ep in EPISODES:
        season = str(ep["season"]).zfill(2)
        episode = str(ep["episode"]).zfill(2)
        tvg_id = f"FreaksGeeks.S{season}E{episode}"
        title = ep["title"]
        url = generate_hls_url(ep["episode_id"])

        m3u.append(
            f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{title}" '
            f'group-title="Freaks and Geeks" type="video", '
            f'S{season}E{episode} • {title}'
        )
        m3u.append(url)
        m3u.append("")  # blank line

    os.makedirs('output', exist_ok=True)
    path = os.path.join('output', 'freaks_and_geeks.m3u')
    with open(path, 'w', encoding='utf-8') as f:
        f.write("\n".join(m3u))
    print(f"Playlist generated: {path}")


if __name__ == '__main__':
    generate_m3u_playlist()
