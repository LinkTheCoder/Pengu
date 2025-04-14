import discord
import json
import random
from discord.ext import commands
from discord import app_commands

# Load quiz data once
with open('data/quiz.json', 'r') as f:
    quiz_data = json.load(f)

class QuizView(discord.ui.View):
    def __init__(self, options, correct_option):
        super().__init__(timeout=15)
        self.correct_option = correct_option
        self.add_buttons(options)

    def add_buttons(self, options):
        for index, option in enumerate(options):
            button = discord.ui.Button(
                label=option['option'],
                style=discord.ButtonStyle.primary,
                custom_id=f'option{index + 1}'
            )

            async def callback(interaction: discord.Interaction, o=option):
                if o.get('isCorrect'):
                    await interaction.response.send_message("✅ Correct answer!", ephemeral=True)
                else:
                    await interaction.response.send_message(
                        f"❌ Incorrect!\nThe correct answer is: **{self.correct_option['option']}**",
                        ephemeral=True
                    )
                self.stop()

            button.callback = callback
            self.add_item(button)

class QuizCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="quiz", description="Get a random penguin quiz")
    async def quiz(self, interaction: discord.Interaction):
        try:
            quizzes = quiz_data['quizzes']
            random_question = random.choice(quizzes)
            question = random_question['question']
            options = random_question['options']
            correct_option = next((opt for opt in options if opt['isCorrect']), None)

            view = QuizView(options, correct_option)
            await interaction.response.send_message(
                content=question, 
                view=view, 
                ephemeral=True  # Make the message visible only to the user
            )

        except Exception as e:
            print(f"Error: {e}")
            await interaction.response.send_message(
                content="⚠️ An error occurred while fetching the quiz data.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(QuizCommand(bot))
