def replace_text(text):
    text = text.replace("baka", "dummy").replace("Baka", "Dummy")
    text = text.replace("{filtered}","bitch")
    text = text.replace("tsundere", "").replace("Tsundere", "")
    return text

if __name__ == "__main__":
    input_text = "{filtered}! How dare you speak to me like that baka!"
    output_text = replace_text(input_text)
    print(f'{output_text}')