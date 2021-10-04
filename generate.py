#!/usr/bin/env python3
import yaml
import json
import os
from pprint import pprint
import jinja2

def hex2rgb(h):
  res = (
    ((h & 0xff0000) >> 4*4) / 256.0,
    ((h & 0x00ff00) >> 4*2) / 256.0,
    ((h & 0x0000ff) >> 4*0) / 256.0
  )
  return res

def main():
  home = os.getenv("HOME")

  with open(f"{home}/.iterm2_profiles.yml", "r") as f:
    yaml_data = yaml.load(f)

  profiles = []
  for name, d in yaml_data["profiles"].items():
    d["name"] = name
    d.update(yaml_data.get("defaults", {}))


    d["red"], d["green"], d["blue"] = hex2rgb(d.get("bg_color", 0x000000))

    for key, value in d.items():
      if isinstance(value, str):
        d[key] = jinja2.Template(value).render(d)

    template = yaml_data["templates"][d["template"]]
    res = jinja2.Template(template).render(d)

    profiles.append(json.loads(res))

  out = {
    "Profiles": profiles
  }

  #print(json.dumps(out, indent=2))

  with open(f"{home}/.iterm2_profiles", "w") as f:
    json.dump(out, f)

if __name__=='__main__':
  main()
