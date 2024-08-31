import nextcord
from nextcord.ext import commands, application_checks
import sqlite3
import math
import time
import webserver
from github import Github
from github import Auth
database = sqlite3.connect("Grades3.sqlite")
cursor = database.cursor()
client: client = nextcord.Client(intents=nextcord.Intents.all(), activity=nextcord.Game(name='tetris'))
g=Auth.Login("CreepercraftYT", "CcYTT99*")
print(g)
repo=g.get_repo("CreepercraftYT/GradeBot")
contents = repo.get_contents("Grades3.sqlite", ref="update")
repo.update_file(contents.path, "update database", "update database", contents.sha, branch="main")


cursor.execute("""CREATE TABLE IF NOT EXISTS main(user_id INTEGER, guild_id INTEGER, exp INTEGER, grade INTEGER, last_grade INTEGER, level INTEGER, difficulty INTEGER, channel_id INTEGER)""")
#cursor.execute("""INSERT INTO main(difficulty) VALUES(1)""")
#cursor.execute("""ALTER TABLE main ADD exam INTEGER INTEGER""")
#cursor.execute("""INSERT INTO main(disable_ranking_message, show_new_grade) VALUES(0, 0)""")
#database.commit()

class Grading(commands.Cog):
    bot = commands.Bot()
    #application_checks = nextcord.applicaton_checks
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        cursor.execute(f"SELECT user_id, guild_id, exp, grade, last_grade, difficulty, level FROM main WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}")
        result = cursor.fetchone()
        if result is None:
            cursor.execute(
                f"SELECT difficulty, grade FROM main WHERE guild_id = {message.guild.id}")
            difficulty = cursor.fetchone()
            if difficulty is None:
                no_message = 0
                show_grade = 0
                difficulty = 0
                cursor.execute(
                    f"INSERT INTO main(user_id, guild_id, exp, grade, last_grade, level, difficulty, disable_ranking_message, show_new_grade, cool, regret) VALUES({message.author.id}, {message.guild.id}, 0, 0, 32, 0, 1, {no_message}, {show_grade}, 0, 0)")
                database.commit()
            else:
                cursor.execute(
                    f"SELECT disable_ranking_message, show_new_grade FROM main WHERE guild_id = {message.guild.id}")
                result = cursor.fetchone()
                no_message = result[0]
                show_grade = result[1]
                difficulty = difficulty[1]
                print(no_message, show_grade, difficulty)
                cursor.execute(f"INSERT INTO main(user_id, guild_id, exp, grade, last_grade, level, difficulty) VALUES({message.author.id}, {message.guild.id}, 0, 0, 32, 0, {difficulty})")
                database.commit()
        else:
            msg = str(message.content)
            print(str(message.author) + ': ' + msg)
            message_length = len(msg)
            print('length: ' + str(message_length))
            exp = result[2]
            grade = result[3]
            last_grade = result[4]
            level = result[6]
            print('level: ' + str(level))
            exp_gain = 0
            print('experience: ' + str(exp), 'grade: ' + str(grade))
            cursor.execute(
                    f"SELECT difficulty, grade FROM main WHERE guild_id = {message.guild.id}")
            result = cursor.fetchone()
            result = result[0]
            if result == 5:
                t = time.gmtime()
                day = time.strftime("%A", t)
                if day == "Sunday":
                    cursor.execute("SELECT * FROM main WHERE guild_id = ? ORDER BY exp DESC")
                    result = cursor.fetchall
                    for i in range(len(result)):
                        user = result[i][0]
                        grade = result[i][3]
                        qualified = result[1][12]
                        exam = result[i][13]
                        if grade > qualified and exam == 0:
                            exam = grade


            else:
                pass

            print('difficulty: ' + str(result))
            easy_exp_thresholds = [10, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 330, 380,
                                   430, 480, 530, 580, 630, 680, 730, 830, 930, 1030, 1130, 1230, 2430]
            normal_exp_thresholds = [40, 80, 140, 200,	350, 550, 800, 1200, 1600, 2200, 3000, 4000, 5200, 6600, 8200, 10000, 12000, 16000, 22000, 30000, 40000, 52000, 66000, 82000, 100000, 120000, 150000, 200000, 230000, 290000, 340000, 400000]
            hard_exp_thresholds = [200,	400,	700,	1000,	1750,	2750,	4000,	6000,	8000,	11000,	15000,	20000,	26000,	33000,	41000,	50000,	60000,	80000,	110000,	150000,	200000,	260000,	330000,	410000,	500000,	600000,	750000,	1000000,	1150000,	1450000,	1700000,	2000000]
            accurate_exp_thresholds = [400, 800, 1400, 2000, 3500, 5500, 8000, 12000, 16000, 22000, 30000, 40000, 52000, 66000, 82000,
                                         100000, 120000, 126000]
            grade_aux = grade
            if grade == 32:
                grade_aux == grade - 1
            print(grade_aux)
            if result == 0:
                exp_threshold = easy_exp_thresholds[grade_aux]
            elif result == 1:
                exp_threshold = normal_exp_thresholds[grade_aux]
            elif result == 2:
                exp_threshold = hard_exp_thresholds[grade_aux]
            else:
                exp_threshold = accurate_exp_thresholds[grade_aux]
            print('experience: ' + str(exp),'threshold: ' + str(exp_threshold),'grade: ' + str(grade))
            if grade <= 8:
                exp_gain = 1
            elif grade <= 17:
                exp_gain = 2
            elif grade <= 26:
                exp_gain = 3
            elif grade <= 31:
                exp_gain = 4
            elif grade == 32:
                exp_gain = 5
            length_mult = 0
            if message_length <= 15:
                length_mult = 1
            elif message_length <= 30:
                length_mult = 2
            elif message_length <= 60:
                length_mult = 3
            elif message_length <= 280:
                length_mult = 4
            elif message_length <= 1499:
                length_mult = 8
            elif message_length >= 1500:
                lenght_mult = 0
            level = level + message_length / 999
            level_mult = 0
            if level < 250:
                level_mult = 0
            elif level < 500:
                level_mult = 1
            elif level < 750:
                level_mult = 2
            else:
                level_mult = 3
            exp += exp_gain * (length_mult + level_mult)
            section  = 0
            print('lenght multiplier: ' + str(length_mult),'level multiplier: ' + str(level_mult))
            floor_level = math.floor(level)
            print(floor_level % 100)
            cursor.execute(
                f"SELECT cool, regret FROM main WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}")
            cool_regret = cursor.fetchone()
            if cool_regret == None:
                cursor.execute(
                    f'UPDATE main SET cool = 0, regret = 0 WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}')
                database.commit()
            cool = cool_regret[0]
            regret = cool_regret[1]
            section = math.floor(floor_level / 100)
            print('section: ' + str(section) + ' cool: ' + str(cool) + ' regret: ' + str(regret) +' grade: ' + str(grade))
            cursor.execute(
                f"SELECT difficulty, grade FROM main WHERE guild_id = {message.guild.id}")
            difficulty = cursor.fetchone()
            difficulty = difficulty[0]
            if floor_level % 100 == 70 and cool == 0 and regret == 0 and difficulty != 4:
                cool_table = [0, 6, 10, 13, 16, 19, 21, 23, 25, 27, 30]
                regret_table = [0, 3, 6, 9, 12, 15, 17, 20, 23, 25, 27]
                section += 1
                print('minimum cool grade: ' + str(cool_table[section]))
                if grade >= cool_table[section]:
                    cool = 1
                    if result == 0:
                        exp = easy_exp_thresholds[grade]
                    elif result == 1:
                        exp = normal_exp_thresholds[grade]
                    elif result == 2:
                        exp = hard_exp_thresholds[grade]
                    elif result == 3:
                        exp = accurate_exp_thresholds[grade]
                    await message.channel.send(f'{message.author} COOL!!')
                elif grade < cool_table[section] and grade > regret_table[section]:
                    pass
                elif grade <= regret_table[section]:
                    print('maximum regret grade: ' + str(regret_table[section]))
                    grade = grade - 1
                    regret = 1
                    if result == 0:
                        exp = easy_exp_thresholds[grade - 1]
                    elif result == 1:
                        exp = normal_exp_thresholds[grade - 1]
                    elif result == 2:
                        exp = hard_exp_thresholds[grade - 1]
                    elif result == 3:
                        exp = accurate_exp_thresholds[grade - 1]
                    await message.channel.send(f'{message.author} REGRET!!')
                cursor.execute(
                    f'UPDATE main SET exp = {exp}, grade = {grade}, level = {level}, cool = {cool}, regret = {regret} WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}')
                database.commit()
            elif floor_level % 100 != 70 and cool == 1 or regret == 1:
                cursor.execute(
                    f'UPDATE main SET cool = 0, regret = 0 WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}')
                database.commit()

            if exp >= exp_threshold and grade != last_grade and difficulty != 4:
                grade += 1
                print('grade: ' + str(grade))
                grade_conversion = ['9', '8', '7', '6', '5', '4', '3', '2', '1', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6',
                                    'S7', 'S8', 'S9', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'Master',
                                    'MasterK', 'MasterV', 'MasterO', 'MasterM', 'GrandMaster']
                accurate_grade_conversion = ['9', '8', '7', '6', '5', '4', '3', '2', '1', 'S1', 'S2', 'S3', 'S4', 'S5',
                                             'S6', 'S7', 'S8', 'S9', 'GM']
                converted_grade = 0
                if result != 3:
                    converted_grade = grade_conversion[grade]
                else:
                    converted_grade = accurate_grade_conversion[grade]
                cursor.execute(
                    f"SELECT disable_ranking_message FROM main WHERE guild_id = {message.guild.id}")
                result = cursor.fetchone()
                result = result[0]
                if result == 0:
                    cursor.execute(
                        f"SELECT show_new_grade FROM main WHERE guild_id = {message.guild.id}")
                    result = cursor.fetchone()
                    result = result[0]
                    if result == 0:
                        await message.channel.send(f'{message.author} ranked up!')
                    else:
                        await message.channel.send(f'{message.author} ranked up to grade {converted_grade}!')
                else:
                    pass
            elif difficulty == 4:
                converted_grade = 0
                hell_grade_conversion = [1, 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13']
                converted_grade = hell_grade_conversion[grade]
                temp_grade = math.floor(level/100)
                print(temp_grade)
                print(level)
                print(grade)
                if grade == temp_grade:
                    pass
                else:
                    grade = temp_grade
                    converted_grade = hell_grade_conversion[grade]
                    cursor.execute(
                    f"SELECT disable_ranking_message FROM main WHERE guild_id = {message.guild.id}")
                    result = cursor.fetchone()
                    result = result[0]
                    if result == 0:
                        cursor.execute(
                        f"SELECT show_new_grade FROM main WHERE guild_id = {message.guild.id}")
                        result = cursor.fetchone()
                        result = result[0]
                        if result == 0:
                            await message.channel.send(f'{message.author} ranked up!')
                        else:
                            await message.channel.send(f'{message.author} ranked up to grade {converted_grade}!')
                    else:
                        pass
            cursor.execute(f'UPDATE main SET exp = {exp}, grade = {grade}, level = {level} WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}')
            database.commit()

    @bot.slash_command(description="main command")
    async def grading(self, interaction: nextcord.Interaction):
        """
        This is the main slash command that will be the prefix of all commands below.
        This will never get called since it has subcommands.
        """
        pass
    @grading.subcommand(description='shows info about how the grading system works')
    async def grade_help(self, interaction: nextcord.Interaction):
        cursor.execute(
            f"SELECT difficulty, grade FROM main WHERE guild_id = {interaction.guild_id}")
        difficulty = cursor.fetchone()
        difficulty = difficulty[0]
        if difficulty != 3:
            await interaction.response.send_message(f"there is a total of 33 grades, these are:"
                                                               " 9, 8, 7, 6, 5, 4, 3, 2, 1, S1, S2, S3, S4, S5, S6, S7, S8, S9, m1, m2, m3, m4, m5, m6, m7, m8, m9, Master, MasterK, MasterV, MasterO, MasterM and Grand Master. "
                                                              "each grade is (sort of) harder to get than the previous one, but if you only get one xp point per message, you'll need to send 400000 (in Normal difficulty, it's 2430 in Easy and 2000000 in Hard) messages to get Grand Master. "
                                                             "so, once reaching S1, you'll get 2 xp points per message, 3 once you reach m1, 4 once you reach Master and 5 once you've reached Grand Master (these values are then multiplied by your multipliers)."
                                                    "there are 2 multipliers: the length multiplier amd the level multiplier. basically, the longer your message and the higher your level, the more xp you get per message")
        else:
            await interaction.response.send_message(f"there is a total of 33 grades, these are:"
                                                    " 9, 8, 7, 6, 5, 4, 3, 2, 1, S1, S2, S3, S4, S5, S6, S7, S8, S9 and Grand Master. "
                                                    "each grade is harder to get than the previous one, but if you only get one xp point per message, you'll need to send 126000 messages to get Grand Master. "
                                                    "so, once reaching S1, you'll get 2 xp points per message and 3 once you've reached Grand Master (these values are then multiplied by your multipliers)."
                                                    "there are 2 multipliers: the length multiplier amd the level multiplier. basically, the longer your message and the higher your level, the more xp you get per message")

    @grading.subcommand(description='shows the required amount of xp for each grade')
    async def xp_requirements(self, interaction: nextcord.Interaction):
        cursor.execute(
            f"SELECT difficulty, grade FROM main WHERE guild_id = {interaction.guild_id}")
        difficulty = cursor.fetchone()
        difficulty = difficulty[0]
        easy_exp_thresholds = [10, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 330, 380,
                               430, 480, 530, 580, 630, 680, 730, 830, 930, 1030, 1130, 1230, 2430]
        normal_exp_thresholds = [40, 80, 140, 200, 350, 550, 800, 1200, 1600, 2200, 3000, 4000, 5200, 6600, 8200, 10000,
                                 12000, 16000, 22000, 30000, 40000, 52000, 66000, 82000, 100000, 120000, 150000, 200000,
                                 230000, 290000, 340000, 400000]
        hard_exp_thresholds = [200, 400, 700, 1000, 1750, 2750, 4000, 6000, 8000, 11000, 15000, 20000, 26000, 33000,
                               41000, 50000, 60000, 80000, 110000, 150000, 200000, 260000, 330000, 410000, 500000,
                               600000, 750000, 1000000, 1150000, 1450000, 1700000, 2000000]
        accurate_exp_thresholds = [400, 800, 1400, 2000, 3500, 5500, 8000, 12000, 16000, 22000, 30000, 40000, 52000,
                                   66000, 82000,
                                   100000, 120000, 126000]
        if difficulty != 3:
            if difficulty == 0:
                await interaction.response.send_message(f'for 8: 10, for 7: 20, for 6: 30, for 5: 40, for 4: 50, for 3: 60, for 2: 70, for 1: 80, for S1: 100, for S2: 120, for S3: 140, for S4: 160, for S5: 180, for S6: 200, for S7: 220, for S8: 240, for S9: 260, for m1: 330, for m2: 380, for m3: 430, for m4: 480, for m5: 530, for m6: 580, for m7: 630, for m8: 680, for m9: 730, for Master: 830, for MasterK: 930, for MasterV: 1030, for MasterO: 1130, for MasterM: 1230, for GrandMaster: 2430.')
            elif difficulty == 1:
                await interaction.response.send_message(f'for 8: 40, for 7: 80, for 6: 140, for 5: 200, for 4: 350, for 3: 550, for 2: 800, for 1: 1200, for S1: 1600, for S2: 2200, for S3: 3000, for S4: 4000, for S5: 5200, for S6: 6600, for S7: 8200, for S8: 10000, for S9: 12000, for m1: 16000, for m2: 22000, for m3: 30000, for m4: 40000, for m5: 52000, for m6: 66000, for m7: 82000, for m8: 100000, for m9: 120000, for Master: 150000, for MasterK: 200000, for MasterV: 230000, for MasterO: 290000, for MasterM: 340000, for GrandMaster: 400000')
            elif difficulty == 2:
                await interaction.response.send_message(f'for 8: 200, for 7: 400, for 6: 700, for 5: 1000, for 4: 1750, for 3: 2750, for 2: 4000, for 1: 6000, for S1: 8000, for S2: 11000, for S3: 15000, for S4: 20000, for S5: 26000, for S6: 33000, for S7: 41000, for S8: 50000, for S9: 60000, for m1: 80000, for m2: 110000, for m3: 150000, for m4: 200000, for m5: 260000, for m6: 330000, for m7: 410000, for m8: 500000, for m9: 600000, for Master: 750000, for MasterK: 1000000, for MasterV: 1150000, for MasterO: 1450000, for MasterM: 1700000, for GrandMaster: 2000000')
        else:
            if difficulty == 3:
                await interaction.response.send_message(f'for 8: 400, for 7: 800, for 6: 1400, for 5: 2000, for 4: 3500, for 3: 5500, for 2: 8000, for 1: 12000, for S1: 16000, for S2: 22000, for S3: 30000, for S4: 40000, for S5: 52000, for S6: 66000, for S7: 82000, for S8: 100000, for S9: 120000, for GrandMaster: 160000')
            elif difficulty == 4:
                await interaction.response.send_message(
                    f'your grade is equal to the first digit of your level')

    @grading.subcommand(description='shows your current xp, grade and rank in the server')
    async def rank(self, interaction: nextcord.Interaction, user: nextcord.Member = nextcord.SlashOption(required=False)):
        rank = 1
        descending = "SELECT * FROM main WHERE guild_id = ? ORDER BY exp DESC"
        cursor.execute(descending, (interaction.guild_id,))
        result = cursor.fetchall()
        for i in range(len(result)):
            if user is None:
                if result[i][0] == interaction.user.id:
                    break
                else:
                    rank += 1
            else:
                if result[i][0] == user.id:
                    break
                else:
                    rank += 1
        if user is None:
            cursor.execute(f'SELECT exp, grade, last_grade, level FROM main WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}')
            result = cursor.fetchone()
            grade = result[1]
            exp = result[0]
            level = math.floor(result[3])
        else:
            cursor.execute(
                f'SELECT exp, grade, last_grade, level FROM main WHERE user_id = {user.id} AND guild_id = {interaction.guild.id}')
            result = cursor.fetchone()
            grade = result[1]
            exp = result[0]
            level = math.floor(result[3])
        normal_exp_thresholds = [40, 80, 140, 200, 350, 550, 800, 1200, 1600, 2200, 3000, 4000, 5200, 6600, 8200, 10000, 12000,
                          16000, 22000, 30000, 40000, 52000, 66000, 82000, 100000, 120000, 150000, 200000, 230000,
                          290000, 340000, 400000]

        if grade != 32:
            next_grade_xp = normal_exp_thresholds[grade]
        grade_conversion = ['9', '8', '7', '6', '5', '4', '3', '2', '1', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'Master','MasterK', 'MasterV', 'MasterO', 'MasterM', 'GrandMaster']
        accurate_grade_conversion = ['9', '8', '7', '6', '5', '4', '3', '2', '1', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'GM']
        hell_grade_conversion = ['1', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6',
                                     'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13']
        cursor.execute(
            f"SELECT difficulty, grade FROM main WHERE guild_id = {interaction.guild_id}")
        difficulty = cursor.fetchone()
        difficulty = difficulty[0]
        if difficulty != 3:
            grade = grade_conversion[grade]
        elif difficulty == 3:
            grade = accurate_grade_conversion[grade]
        elif difficulty == 4:
            grade = hell_grade_conversion[grade]
        print(grade)
        if grade != "GrandMaster":
            if user is None:
                await interaction.response.send_message(f'{interaction.user.mention} you have {exp} exp, your level is {level}, your grade is {grade} and you\'re ranked number {rank} in the server')
            else:
                await interaction.response.send_message(
                    f'{user} has {exp} exp, his/her level is {level}, his/her grade is {grade} and he/she is ranked number {rank} in the server')
        else:
            if user is None:
                await interaction.response.send_message(
                f'{interaction.user.mention} you have {exp} exp, your level is {level}, you are Grand Master! and you\'re ranked number {rank} in the server')
            else:
                await interaction.response.send_message(
                    f'{user} has {exp} exp, his/her level is {level}, his/her grade is {grade} and he/she is ranked number {rank} in the server')

    @grading.subcommand(description='change how hard is it to rank up in your server')
    @application_checks.has_guild_permissions(ban_members=True)
    async def difficulty(self, interaction: nextcord.Interaction, difficulty: int = nextcord.SlashOption(name="difficulty", description='Pick the difficulty, be careful, you can\'t change it again', choices={'Easy': 0, 'Normal': 1, 'Hard': 2, "Accurate": 3, "Hell": 4},),): #confirm: int = nextcord.SlashOption(name='confirm?', description='ARE YOU SURE???? Once you change the difficulty, you can\'t change it again!', choices={'yes': 1, 'no': 0},),):
        cursor.execute(
            f"SELECT difficulty, grade FROM main WHERE guild_id = {interaction.guild_id}")
        result = cursor.fetchone()
        print(result)
        print(difficulty)
        dif = result[0]
        if dif != 1:
            await interaction.response.send_message(f'you already changed the difficulty, sorry')
            pass
        else:
            if difficulty != 3:
             cursor.execute(
                f'UPDATE main SET difficulty = {difficulty} WHERE guild_id = {interaction.guild_id}')
             database.commit()
             await interaction.response.send_message(f'difficulty was changed successfully')
            else:
                cursor.execute(
                    f'UPDATE main SET difficulty = {difficulty}, last_grade = 17 WHERE guild_id = {interaction.guild_id}')
                database.commit()
                await interaction.response.send_message(f'difficulty was changed successfully')

    @grading.subcommand(description='shows the difficulty set for the server')
    async def server_diff(self, interaction: nextcord.Interaction):
        cursor.execute(
            f"SELECT difficulty, grade FROM main WHERE guild_id = {interaction.guild_id}")
        result = cursor.fetchone()
        print(result)
        result = result[0]
        if result == 0:
            await interaction.response.send_message(f"the difficulty on this server is set to Easy")
        elif result == 1:
            await interaction.response.send_message(f"the difficulty on this server is set to Normal")
        elif result == 2:
            await interaction.response.send_message(f"the difficulty on this server is set to Hard")
        elif result == 3:
            await interaction.response.send_message(f'the difficulty on this server is set to Accurate')
        elif result == 4:
            await interaction.response.send_message(f'the difficulty on this server is set to Hell')

    @grading.subcommand(description="reset subcommand group")
    async def reset(self, interaction: nextcord.Interaction):
        """
        This is a subcommand group of the '/main' slash command.
        All subcommands of this group will be prefixed with '/main main_group'.
        This will never get called since it has subcommands.
        """
        pass

    @reset.subcommand(description="Resets everything back to normal, including the difficulty")
    @application_checks.has_guild_permissions(ban_members=True)
    async def server(self, interaction: nextcord.Interaction):
        cursor.execute(
                f'UPDATE main SET exp = 0, grade = 0, last_grade = 32, level = 0, difficulty = 1 WHERE guild_id = {interaction.guild_id}')
        database.commit()
        await interaction.response.send_message("The server was reset")

    @reset.subcommand(description="Resets the user's exp, level and grade")
    async def user(self, interaction: nextcord.Interaction):
        cursor.execute(
                f'UPDATE main SET exp = 0, grade = 0, last_grade = 32, level = 0 WHERE user_id = {interaction.user.id} and guild_id = {interaction.guild_id}')
        database.commit()
        await interaction.response.send_message("Your progress was reset")

    @bot.slash_command(description="utility")
    async def utility(self, interaction: nextcord.Interaction):
        """
        This is the main slash command that will be the prefix of all commands below.
        This will never get called since it has subcommands.
        """
        pass

    @utility.subcommand(description='toggle whether the "ranked up!" message is sent or not')
    @application_checks.has_guild_permissions(ban_members = True)
    async def toggle_message(self, interaction: nextcord.Interaction):
           #await interaction.response.send_message(f'SoonTM')
           #raise NotImplementedError('SoonTM')
           cursor.execute(
               f"SELECT disable_ranking_message FROM main WHERE guild_id = {interaction.guild_id}")
           result = cursor.fetchone()
           result = result[0]
           if result == 0:
               cursor.execute(f'UPDATE main SET disable_ranking_message = 1 WHERE guild_id = {interaction.guild_id}')
               database.commit()
               await interaction.response.send_message(f'the "ranked up!" message was disabled, use the same command to enable it again')
           else:
               cursor.execute(f'UPDATE main SET disable_ranking_message = 0 WHERE guild_id = {interaction.guild_id}')
               database.commit()
               await interaction.response.send_message(
                   f'the "ranked up!" message was enabled, use the same command to disable it again')

    @utility.subcommand(description='toggle whether the "ranked up!" message includes the grade the user ranked up to or not')
    @application_checks.has_guild_permissions(ban_members=True)
    async def display_new_grade(self, interaction: nextcord.Interaction):
        # await interaction.response.send_message(f'SoonTM')
        # raise NotImplementedError('SoonTM')
        cursor.execute(
            f"SELECT show_new_grade FROM main WHERE guild_id = {interaction.guild_id}")
        result = cursor.fetchone()
        result = result[0]
        if result == 0:
            cursor.execute(f'UPDATE main SET show_new_grade = 1 WHERE guild_id = {interaction.guild_id}')
            database.commit()
            await interaction.response.send_message(
                f'the new user grade will now show on the "ranked up!" message, use the same command to disable it again')
        else:
            cursor.execute(f'UPDATE main SET show_new_grade = 0 WHERE guild_id = {interaction.guild_id}')
            database.commit()
            await interaction.response.send_message(
                f'the new user grade will no longer show on the "ranked up!" message use the same command to enable it again')

    #@utility.subcommand(description='change the channel where the "ranked up!" message is sent')
    #@application_checks.has_guild_permissions(ban_members = True)
    #async def channel(self, interaction: nextcord.Interaction, where: Channel[int]):
    #        #await interaction.response.send_message(f'SoonTM')
    #        #raise NotImplementedError('SoonTM')
    #        cursor.execute(f'UPDATE main SET channel_id = {where} WHERE guild_id = {interaction.guild_id}')
    #        database.commit()
    #        await interaction.response.send_message(f'channel was changed succesfully')


def setup(bot):
    bot.add_cog(Grading(bot))












































































































