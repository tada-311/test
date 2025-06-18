from pyproj import Transformer
from geopy.distance import geodesic




# ※入力必要箇所（他は入力不要）
easting = 0 # Y座標を入力
northing = 0 # X座標を入力
zone = 0  # 自動で系番号を判別する場合は0、系番号がわかっている場合は1~19で入力




# 日本の緯度経度範囲
japan_bounds = {
    "lat_min": 20.0,
    "lat_max": 46.0,
    "lon_min": 122.0,
    "lon_max": 154.0
}




# 自動判別処理
def auto_detect_zone(easting, northing):
    candidates = []
    for z in range(1, 20):
        epsg_code = 6660 + z
        try:
            transformer = Transformer.from_crs(f"EPSG:{epsg_code}", "EPSG:4326", always_xy=True)
            lon, lat = transformer.transform(easting, northing)




            if (japan_bounds["lat_min"] <= lat <= japan_bounds["lat_max"] and
                japan_bounds["lon_min"] <= lon <= japan_bounds["lon_max"]):
                candidates.append({
                    "zone": z,
                    "epsg": epsg_code,
                    "lat": lat,
                    "lon": lon
                })
        except Exception:
            continue




    if not candidates:
        return None




    reference_point = (33.5, 131.0)
    for c in candidates:
        c["distance"] = geodesic((c["lat"], c["lon"]), reference_point).meters




    best = min(candidates, key=lambda x: x["distance"])
    best["auto_detected"] = True  # 自動判別フラグ
    return best




# メイン処理
result = None




if easting != 0 and northing != 0:
    if zone == 0:
        result = auto_detect_zone(easting, northing)
    elif 1 <= zone <= 19:
        try:
            epsg_code = 6660 + zone
            transformer = Transformer.from_crs(f"EPSG:{epsg_code}", "EPSG:4326", always_xy=True)
            lon, lat = transformer.transform(easting, northing)
            if (japan_bounds["lat_min"] <= lat <= japan_bounds["lat_max"] and
                japan_bounds["lon_min"] <= lon <= japan_bounds["lon_max"]):
                result = {
                    "zone": zone,
                    "epsg": epsg_code,
                    "lat": lat,
                    "lon": lon,
                    "auto_detected": False
                }
        except Exception:
            result = None




# 結果表示
if result:
    print("=== 変換結果（WGS84） ===")
    print(f"系番号: 第{result['zone']}系")
    print(f"EPSGコード: {result['epsg']}")
    print(f"緯度（北緯）: {result['lat']:.10f}")
    print(f"経度（東経）: {result['lon']:.10f}")
    if result.get("auto_detected", False):
        print("※ 系番号は自動で選ばれたものです。")
else:
    print("※ 有効な座標変換結果が得られませんでした。座標または系番号が正しいか確認してください。")

