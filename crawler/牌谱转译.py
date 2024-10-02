"""
这个程序用于将牌谱网址翻译成json文件，基于浏览器工具操作
打开浏览器后需要你输入账号和密码登陆《雀魂》才可以开始下载
"""
import os
import time
import json
from selenium import webdriver # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore

# 如果 ChromeDriver 已添加到 PATH，可以直接初始化
current_dir = os.path.dirname(os.path.abspath(__file__))
chromedriver_path = os.path.join(current_dir, 'chromedriver/chromedriver')

options = webdriver.ChromeOptions()
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(options=options,service=service)

# 打开一个网页
driver.get("https://game.maj-soul.com/1/")
time.sleep(40)
# 手动登陆雀魂网站
# 242300983@qq.com
def execute_script(driver, uuid):
    # JavaScript 脚本与之前控制台中输入的脚本相同
    script = '''
        function paifu(uuid=""){if(!uuid){uuid=prompt("Please Enter a UUID.")}if(!uuid){return}uuid=uuid.replace(/^.*=(.*)_a.*$/,'$1');const pbWrapper=net.ProtobufManager.lookupType(".lq.Wrapper");const pbGameDetailRecords=net.ProtobufManager.lookupType(".lq.GameDetailRecords");function parseRecords(gameDetailRecords,json){try{if(gameDetailRecords.version==0){for(let i in gameDetailRecords.records){const record=(pbWrapper.decode(gameDetailRecords.records[i]));const pb=net.ProtobufManager.lookupType(record.name);const data=JSON.parse(JSON.stringify((pb.decode(record.data))));json.records[i]={name:record.name,data:data}}}else if(gameDetailRecords.version==210715){for(let i in gameDetailRecords.actions){if(gameDetailRecords.actions[i].type==1){const record=(pbWrapper.decode(gameDetailRecords.actions[i].result));const pb=net.ProtobufManager.lookupType(record.name);const data=JSON.parse(JSON.stringify((pb.decode(record.data))));json.actions[i].result={name:record.name,data:data}}}}else{throw("Unknown version: "+gameDetailRecords.version);}}catch(e){console.log(e)}return json}async function fetchData(url){const response=await fetch(url);const arrayBuffer=await response.arrayBuffer();return new Uint8Array(arrayBuffer)}function download(data,uuid){let a=document.createElement("a");a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,"  ")],{type:"text/plain"}));a.download="paifu_"+uuid+".json";a.style.display="none";document.body.appendChild(a);a.click();document.body.removeChild(a)}app.NetAgent.sendReq2Lobby("Lobby","fetchGameRecord",{game_uuid:uuid,client_version_string:GameMgr.Inst.getClientVersion()},async function(error,gameRecord){if(gameRecord.data==""){gameRecord.data=await fetchData(gameRecord.data_url)}const gameDetailRecordsWrapper=pbWrapper.decode(gameRecord.data);const gameDetailRecords=pbGameDetailRecords.decode(gameDetailRecordsWrapper.data);let gameDetailRecordsJson=JSON.parse(JSON.stringify(gameDetailRecords));gameDetailRecordsJson=parseRecords(gameDetailRecords,gameDetailRecordsJson);gameRecord.data="";let gameRecordJson=JSON.parse(JSON.stringify(gameRecord));gameRecordJson.data={name:gameDetailRecordsWrapper.name,data:gameDetailRecordsJson};download(gameRecordJson,uuid)})}
    '''
    uuid_str = json.dumps(uuid)
    # 执行 JavaScript 脚本
    driver.execute_script(script+f"paifu({uuid_str})" )
print("test")
input_file = "混沌恶.html"
with open(input_file,"r") as f:
    for i,uuid in enumerate(f):
        if i<500:
            continue
        if i>700 :
            break
        uuid = uuid.strip()  # 去掉行末的换行符和空格
        execute_script(driver, uuid)
        if i == 500+10:
            time.sleep(5)
        time.sleep(0.4)
        

time.sleep(15)
print("test")
time.sleep(30)
# 关闭浏览器
driver.quit()

