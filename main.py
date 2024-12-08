import nextcord, json, requests, re, certifi, httpx
from nextcord.ext import commands
import time
import os
import datetime
from nextcord import Embed, Color


bot, config = commands.Bot(command_prefix='flexzy!',help_command=None,intents=nextcord.Intents.all()), json.load(open('./config.json', 'r', encoding='utf-8'))

import asyncio




class MyEmbed(Embed):
    def __init__(self, bot):
        self.bot = bot

    def __init__(self, userId: int, amount: str, roleid: str, typepay: int):
        super().__init__(
            description=                                f" แจ้งการซื้อสินค้าสำเร็จ [ {typepay} ] <a:botsever60:1315188577356746812> \n\n"
                                f"<a:botsever60:1308698587429076992> `ผู้ใช้` `:` <@{userId}>\n\n"
                                f"<a:botsever60:1309014332478197770> `ราคายศ` `:` `{amount}` \n\n"
                                f"<a:botsever60:1315187052576374995> `ได้รับยศ` `:` <@&{roleid}> \n\n"
                                f"> ซื้อยศสำเร็จ รหัสจะอยู่ที่ห้อง <#1309056629400010772> <a:botsever60:1309014917738790983>\n\n"
                                f"> ขอบคุณที่สนับสนุนเซิร์ฟเวอร์ของเรา <a:botsever60:1315187089419276448> "
        )
        self.color = 0x12ff00
        user = bot.get_user(int(userId))
        if user.avatar:
                self.set_thumbnail(url=user.avatar.url)
                self.set_image(url="https://img5.pic.in.th/file/secure-sv1/PB-Scarlet-Banner677b539260c7104d.gif")

class BuyModal(nextcord.ui.Modal) :

   def __init__(self):
        super().__init__('กรอกลิ้งค์อั่งเปาของท่าน')
        self.a = nextcord.ui.TextInput(
            label = 'Truemoney Wallet Angpao',
            placeholder = 'https://gift.truemoney.com/campaign/?v=xxxxxxxxxxxxxxx',
            style = nextcord.TextInputStyle.short,
            required = True
        )
        self.add_item(self.a)

   async def callback(self, interaction: nextcord.Interaction):
        link = str(self.a.value).replace(' ', '')
        data = {
            'phone': config['phone'],
            'gift_link': link
        }
        try:
            res = requests.post("https://byshop.me/api/truewallet", data=data)
            res.raise_for_status()  # Raises an error for bad responses
        except requests.RequestException as e:
            embed = nextcord.Embed(description=f'เกิดข้อผิดพลาดในการเชื่อมต่อ: {str(e)}', color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        response_data = res.json()
        print(response_data)
        status = response_data.get('status')
        message = response_data.get('message')
        amount = int(float(response_data.get('amount')))


        phone = response_data.get('phone')
        gift_link = response_data.get('gift_link')
        time = response_data.get('time')

        if status == "success":
            amount = int(amount)
            for roleData in config['roleSettings']:
                if (amount == roleData['price']):
                    role = nextcord.utils.get(interaction.user.guild.roles, id=int(roleData['roleId']))
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(content=f"✅ ทางเราแอดให้แล้วขอบพระคุณมาก เช็ครายละเอียดได้ที่ <#{config['channelLog']}> <@{interaction.user.id}>**", ephemeral=True)

                    await bot.get_channel(int(config['channelLog'])).send(embed=MyEmbed(interaction.user.id, amount, role.id, "ซองอั๋งเป๋า"))
        else:
            embed = nextcord.Embed(description='ต้องมีอะไรผิดพลาดตรงไหนนนนนนนนนนนนน', color=nextcord.Color.from_rgb(255, 0, 0))
            await interaction.response.send_message(embed=embed, ephemeral=True)






class BuyView(nextcord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(nextcord.ui.Button(style=nextcord.ButtonStyle.link, label="ติดต่อ",emoji="<a:botsever60:1309014917738790983>", url="https://discord.com/channels/416274780254109696/416274780254109698"))

    @nextcord.ui.button(label='︲ เติมเงิน',emoji="<a:botsever60:1309014941335945216>", custom_id='buyRole', style=nextcord.ButtonStyle.blurple)
    async def buyRole(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(BuyModal())

    @nextcord.ui.button(label='︲ราคายศทั้งหมด',emoji="<a:botsever60:1308701050123063336>", custom_id='priceRole', style=nextcord.ButtonStyle.green)
    async def priceRole(self, button: nextcord.Button, interaction: nextcord.Interaction):
        description = ''
        for roleData in config['roleSettings']:
            description += f'เติมเงิน {roleData["price"]} บาท จะได้รับยศ\n 𓆩⟡𓆪  <@&{roleData["roleId"]}> <a:botsever60:1309014886063276032>   \n₊✧────────────────✧₊∘\n'
        embed = nextcord.Embed(
            title='<a:botsever60:1308698246675304458>  ราคายศทั้งหมด  <a:botsever60:1309014869021822986>  ',
            color=nextcord.Color.from_rgb(93, 176, 242),
            description=description
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

class setupView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label='︲เซฟยศ',
                        emoji="<a:botsever60:1184927829893337158>",
                        custom_id='market12',
                        style=nextcord.ButtonStyle.gray,
                        row=2)
    async def market12(self, button: nextcord.Button,
                        interaction: nextcord.Interaction):
                user = interaction.user
                role_data = [role.name for role in user.roles if "@everyone" not in role.name]
                file_path = f"saveroles/role_{user.name}.json"

                try:
                    with open(file_path, "w", encoding='utf-8') as f:
                        json.dump(role_data, f)
                except Exception as e:
                    print(f"Error saving roles: {e}")
                    await interaction.response.send_message("An error occurred while saving roles.", ephemeral=True)
                    return
                embed = nextcord.Embed(title="บันทึกยศที่เซฟ", color=0xdddddd)
                embed.set_author(icon_url=interaction.guild.icon, name="ระบบขายสินค้า V5 By PB SCARLET SHOP")
                embed.set_footer(icon_url=None, text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                if interaction.user.avatar:
                        embed.set_thumbnail(url=interaction.user.avatar.url)
                else :
                        embed.set_thumbnail(url=None)
                if user.avatar:
                    embed.set_author(name="ระบบเชฟยศอัติโนมัติ", url="", icon_url=user.avatar)     
                formatted_roles = "\n".join(role_data)
                embed.add_field(name="ยศที่เชฟเสร็จสิ้น", value=f"```\n{formatted_roles}```", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)

            

    @nextcord.ui.button(label='︲รับยศคืน',
                        emoji="<a:botsever59:1309737899838668860>",
                        custom_id='market13',
                        style=nextcord.ButtonStyle.green,
                        row=2)
    async def market13(self, button: nextcord.Button,
                        interaction: nextcord.Interaction):
        user = interaction.user
        file_path = f"saveroles/role_{user.name}.json"
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                role_data = json.load(f)
                for role_name in role_data:
                    roles = nextcord.utils.get(interaction.guild.roles, name=role_name)
                    await user.add_roles(roles)
            await interaction.response.send_message("```diff\n+ คืนยศให้คุณเรียบร้อยแล้ว\n```", ephemeral=True)
        except FileNotFoundError:
            await interaction.response.send_message("```diff\n- ขออภัยไม่มีข้อมูลของคุณ```", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"```diff\n- เกิดข้อผิดพลาด: {e}\n```", ephemeral=True)
@bot.event
async def on_ready():
    bot.add_view(BuyView())
    bot.add_view(setupView())
    print(f"""          LOGIN AS: {bot.user}
    Successfully reloaded application [/] commands.""")


 
@bot.slash_command(name='setup',description='✨ ติดตั้งระบบขายยศ')
async def setup(interaction: nextcord.Interaction):
    if (int(interaction.user.id) == int(config['ownerId'])):
        await interaction.channel.send(embed=nextcord.Embed(
            title=f'<a:botsever60:1309014615207710790>    {interaction.guild.name}  <a:botsever60:1309014615207710790> ',
            description='> <a:botsever60:1309014621079736381>  **ระบบซื้อยศอัติโนมัติ [ 24 ชั่วโมง ] <a:botsever60:1309014621079736381>   **  \n\n```diff\n+ กดปุ่ม "เติมเงินซื้อยศ" เพื่อซื้อยศ      ```\n```diff\n- กดปุ่ม "ราคายศทั้งหมด" เพื่อดูราคายศ  ```\n> <a:botsever60:1308700826423918644> `เติมเงินตามราคายศที่ตั้งไว้ (ยศเข้าตัวทันที)` <a:botsever60:1308700826423918644>     ',
            color=nextcord.Color.blue(),
        ).set_thumbnail(url=interaction.user.avatar)
        .set_footer(text=f"{interaction.guild.name}  | SHOP By ADMIN SCARLET", icon_url=interaction.user.avatar)
        .set_image(url="https://media.discordapp.net/attachments/1201027737004019782/1244129061194829897/unknown_3.jpg?ex=66a9ae7a&is=66a85cfa&hm=4ba1c4929589e76fefb10b08a1d1c86bf54c5de07aa7ce7673ace1fde7553335&=&format=webp&width=1313&height=656")
        , view=BuyView())
        await interaction.response.send_message((
        'Successfully reloaded application [/] commands.'
        ), ephemeral=True)
    else:
        await interaction.response.send_message((
           'มึงไม่ได้เป็น Owner ไอควาย ใช้ไม่ได้'
        ), ephemeral=True)

@bot.slash_command(name='setupsaverole',description='✨ ติดตั้งระบบเชฟยศ')
async def setup(interaction: nextcord.Interaction):
    if (int(interaction.user.id) == int(config['ownerId'])):
      embed=nextcord.Embed(title="✨ บอทเชฟยศอัติโนมัติ กันหลุดดิส",description="",color=0xff2c2c)
      embed.set_author(name="🪷", url="", icon_url=interaction.guild.icon)  
      embed.add_field(name="`🟢` คนยังไม่เคยเซฟ `🟢`", value="```diff\n+ ให้กดปุ่ม (เซฟข้อมูลผู้ใช้) เพื่อทำการเก็บข้อมูล\n```", inline=True)
      embed.add_field(name="`🟢` คนมาเอายศคืน `🟢`", value="```diff\n+ ให้กดปุ่ม (รับยศคืน) เพื่อรับยศคืนในกรณีดิสบิน\n+ เผลอออกดิส หรือดิสหลุด หรืออยากออกเข้าใหม่```", inline=True)
      embed.add_field(name="`❗` ข้อความจากแอดมิน `❗`", value="```diff\n- ❗ : บอทมีปัญหาโปรดแจ้งแอดมินโดยทันที\n```", inline=False)
      embed.set_image(url="https://media.discordapp.net/attachments/1168490971990851645/1168892040562610278/standard.gif?ex=659d3e8b&is=658ac98b&hm=e69154a948fe7643d1a937f434e454f73fe55054c4e537ea214fda83ec983529&=")
      embed.set_image(url="https://media.discordapp.net/attachments/1168490971990851645/1168892040562610278/standard.gif?ex=65afb38b&is=659d3e8b&hm=7b3a9b1a593ef37cacfabb0d5d23086507dde08d4563b42c8bb22f60a527f9dc&=&width=585&height=75")
      await interaction.channel.send(embed=embed,view=setupView())
    else:
        await interaction.response.send_message((
           'มึงไม่ได้เป็น Owner ไอควาย ใช้ไม่ได้'
        ), ephemeral=True)


bot.run(config['token'])