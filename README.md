## iterm2_profiles_generator

This is a script for iterm2 users to generate profiles.

I ssh into a great many computers throughout the day.  I keep them organized and easily accessible by creating an `.iterm2_profiles` file in my home directory.  In iterm, I merely need to hit shift-command-O and start typing the name of the host I wish to connect to.  Hit enter, and the host to which I want to connect will open in a new tab (with tmux attached and ready to go).

Whether you have a similar workflow, or just want to make it easier to open local profiles you can use this script.

### Instructions

1. **Back up your `.iterm2_profiles` file if you have one**
1. Create a `~/.iterm2_profiles.yml` file in your home directory and fill it appropriately.
1. Run the included script, and a new `.iterm2_profiles` file will be generated for you.

### `.iterm2_profiles.yml`

Here's an annotated simple example

```
# ALL profiles will have these keys mixed in
defaults:
  template: ssh_template

# You can selectively mix dictionaries into your profiles using YAML anchor and alias syntax
mixins:
  fancy: &fancy
    bg_color: 0x400000

templates:
  ssh_template: |
    {
      "Name": "{{name}}",
      "Guid": "{{name}}",
      "Command" : "ssh {{ssh}} {{options}}",
      "Custom Command" : "Yes",
      "Background Color": {
        "Red Component": {{red}},
        "Green Component": {{green}},
        "Blue Component": {{blue}}
      },
      "Dynamic Profile Parent Name": "my_profile"
    }

profiles:
  host_1:
    <<: *fancy
    ssh: user@host_1.company.com
    options: "-o'StrictHostKeyChecking=no'"
  host_2:
    <<: *fancy
    ssh: user@host_2.company.com

```

This YAML will generate a file with two profiles, for `host_1` and `host_2`.  They'll both be generated from the `ssh_template` chunk of JSON.  They use that template because `defaults` is mixed in to each of the profiles first.


```
# ALL profiles will have these keys mixed in
defaults:
  template: ssh

# You can selectively mix dictionaries into your profiles using YAML anchor and alias syntax
mixins:
  tmux: &tmux
    command: "tmux a -t main || tmux new {%if directory%} -c {{directory}} {%endif%} -s main"

templates:
  ssh: |
    {
      "Name": "{{name}}",
      "Guid": "{{name}}",
      "Command" : "ssh {{ssh}} {%if port%} -p {{port}} {%endif%}{{options}} {%for item in local_ports%} -L{{item}} {%endfor%} {%for item in remote_ports%} -R{{item}} {%endfor%} -t '{{command}}'",
      "Custom Command" : "Yes",
      "Background Color": {
        "Red Component": {{red}},
        "Green Component": {{green}},
        "Blue Component": {{blue}}
      },
      "Dynamic Profile Parent Name": "ssh"
    }

profiles:
  my_host:
    <<: *tmux
    ssh: ubuntu@my_host.company.io

  my-other-host:
    <<: *tmux
    port: 22221
    directory: /opt/working_directory
    local_ports:
      - "5902:10.0.0.2:5900"
      - "8080:10.0.0.1:80"

```

### Notes

- Every string-valued element in a profile dict is individually formatted using Jinja2.  The resulting items are then formatted using the JSON template.  This allows you to have command strings that rely on other dictionary values.
- The `bg_color` handling is special.  The `red, green, blue` constants will be generated in Python from the hex value.


