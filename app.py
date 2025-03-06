from flask import Flask, request, jsonify, send_from_directory,  render_template
import requests
from flask_cors import CORS
import os
import logging

app = Flask(__name__)
# 增强CORS配置
CORS(app, resources={
    r"/geocode": {
        "origins": ["http://localhost:*", "121.40.93.94"],
        "methods": ["POST"],
        "allow_headers": ["Content-Type"]
    }
})

NOMINATIM_URL = "https://restapi.amap.com/v3/geocode/regeo"

logging.basicConfig(level=logging.ERROR)

# 主页路由
#@app.route('/templates')
#def index():
#    return send_from_directory(app.static_folder, 'index.html')
@app.route('/')
def home():
    return render_template('index.html')

# 地理编码API
def reverse_geocode(lon, lat, api_key):
    try:
        params = {
            'location': f"{lon},{lat}",
            'radius': 100,
            'extensions': 'base',
            'key': api_key
        }
        headers = {
            'User-Agent': 'HugeGeoCodeApp/1.0'
        }
        response = requests.get(NOMINATIM_URL, params=params, timeout=(5, 10))
        response.raise_for_status()
        data = response.json()
        if data.get('status') == '1' and 'regeocode' in data:
            address = data['regeocode']['formatted_address']
            components = data['regeocode']['addressComponent']
            return {
                'lon': lon,
                'lat': lat,
                'address': address,
                'country': components.get('country', ''),
                'province': components.get('province', ''),
                'city': components.get('city') or components.get('province', ''),
                'district': components.get('district', ''),
                'street': components.get('township', '')
            }
        else:
            if data.get('status') != '1' or 'regeocode' not in data:
                logging.error(f"逆地理编码失败: {data.get('info', '未知错误')}")
                results.append({
                    'lon': lon,
                    'lat': lat,
                    'error': data.get('info', '未知错误')
                })
    except requests.RequestException as e:
        return {
            'error': f"网络请求错误: {str(e)}"
        }
    except ValueError as e:
        return {
            'error': f"坐标解析错误: {str(e)}"
        }
    except Exception as e:
        return {
            'error': f"未知错误: {str(e)}"
        }

@app.route('/geocode', methods=['POST'])
def geocode():
    coordinates = request.json.get('coordinates', [])
    # 新增过滤逻辑：移除空行和仅空白字符的行
    coordinates = [c.strip() for c in coordinates if c.strip()]
    api_key = request.json.get('apiKey', '')
    results = []
    
    for coord in coordinates:
        try:
            lon, lat = map(float, coord.split(','))
            params = {
                'location': f"{lon},{lat}",
                'radius': 100,
                'extensions': 'base',
                'key': api_key
            }
            headers = {
                'User-Agent': 'HugeGeoCodeApp/1.0'
            }
            response = requests.get(NOMINATIM_URL, params=params, timeout=(5, 10))
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()
            if data.get('status') == '1' and 'regeocode' in data:
                address = data['regeocode']['formatted_address']
                components = data['regeocode']['addressComponent']
                results.append({
                    'lon': lon,
                    'lat': lat,
                    'address': address,
                    'country': components.get('country', ''),
                    'province': components.get('province', ''),
                    'city': components.get('city') or components.get('province', ''),
                    'district': components.get('district', ''),
                    'street': components.get('township', '')
                })
            else:
                print(f"逆地理编码失败: {data.get('info', '未知错误')}")
                results.append({
                    'lon': lon,
                    'lat': lat,
                    'error': data.get('info', '未知错误')
                })
        except requests.RequestException as e:
            results.append({
                'error': f"网络请求错误: {str(e)}"
            })
        except ValueError as e:
            results.append({
                'error': f"坐标解析错误: {str(e)}"
            })
        except Exception as e:
            results.append({
                'error': f"未知错误: {str(e)}"
            })
    return jsonify(results)

# 静态文件路由
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)