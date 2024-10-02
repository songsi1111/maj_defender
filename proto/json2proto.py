"""
这个程序用于将《雀魂》的liqi.json翻译成liqi.proto
"""
import json

def parse_message(message,name,outfile,nest=0):
    assert("fields" in message)
    for key in message.keys():
        if key not in ["fields", "nested"]:
            raise ValueError(f"Error: {key} key does not exist in the message") # 不认识的键
    o.write("\n"+" "*4*nest+"message "+name+" {\n\n")
    for key in message["fields"]:
        message_field = message["fields"][key]
        for subkey in message_field.keys():
            if subkey not in ["rule", "type", "id"]:
                raise ValueError(f"Error:  {name} key {subkey} does not exist in the message") # 不认识的键
        if "rule" in message_field.keys():
            type = message_field["rule"]+" "+message_field["type"]
        else:
            type = message_field["type"]
        o.write(f"{" "*4*(nest+1)}{type} {key} = {str(message_field["id"])};\n")
    if "nested" in message:
        for key in message["nested"].keys():
            parse_message(message["nested"][key],key,outfile,nest+1)
    o.write(" "*4*nest+"}\n")
    # o.write(message.keys())
def parse_service(service, name, outfile):
    outfile.write(f"\nservice {name} {{\n")
    
    for method_name, method_info in service["methods"].items():
        for key in method_info.keys():
            if key not in ["requestType", "responseType"]:
                raise ValueError(f"Error: {key} key does not exist in the message") # 不认识的键
        request_type = method_info["requestType"]
        response_type = method_info["responseType"]
        outfile.write(f'{" "*4}rpc {method_name} ({request_type}) returns ({response_type});\n')

    outfile.write("}\n")
def parse_enum(enum, name, outfile):
    assert("values" in message)
    outfile.write(f"\nenum {name} {{\n\n")
    
    for key, value in enum["values"].items():
        outfile.write(f'\t{key} = {value};\n')
    
    outfile.write("}\n")

# 读取 JSON 文件
with open("proto/liqi2.json") as i:
    json_file = json.load(i)
    with open("proto/output.proto",'w') as o:
        o.write(f"syntax = \"proto3\";\n\n")
        o.write(f"package {''.join(json_file["nested"].keys())};\n")
        messages = json_file["nested"]["lq"]["nested"]
        for key in messages.keys():
            message=messages[key]
            first_key = next(iter(message.keys()))
            if first_key == "fields":   # message
                parse_message(message,key,o)
            elif first_key == "methods":# service
                parse_service(message,key,o)
            elif first_key == "values": # enum
                parse_enum(message,key,o)
            else:
                print(f"Warning:Unknown Key-{first_key}")
