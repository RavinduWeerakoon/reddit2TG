
import telegram
from reddit import RedditScraper, parse_img_from_text, markdown_to_html, check_question
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from const import *
from database import PrevPosts


prev_posts = PrevPosts()



async def hot(context: ContextTypes.DEFAULT_TYPE):
    #creating the temp list to update the db
    to_update = []
    scraper = RedditScraper()
    hot = scraper.get_hot(num=40)
    last_urls = prev_posts.get_last_urls()

    for post in hot:
        if post.url not in last_urls:
            
            title = post.title
            text = post.selftext
            #exclude pinned messages
            if post.stickied or check_question(post):
                continue
            to_update.append(post.url)
            if post.is_self:
                if "preview.redd.it" in text:
                    send_images(title, text, context)
                else:
                    try:
                        await context.bot.send_message(chatID, text=f"<b>{title}</b>\n\n{markdown_to_html(post.selftext)}", parse_mode=telegram.constants.ParseMode.HTML)
                    except:
                        pass


            elif  '.jpg' in post.url or '.png' in post.url:
                await context.bot.sendPhoto(chatID, photo=post.url, caption=f"<b>{title}</b>", parse_mode=telegram.constants.ParseMode.HTML)
            elif 'reddit.com/gallery' in post.url:
                continue
            
            else:
                await context.bot.send_message(chatID,text=f"<b>{title}</b>\n\n{post.url}", parse_mode=telegram.constants.ParseMode.HTML)
    prev_posts.insert_urls(to_update)        

# async def send_messages(id, text, context):
#     if len(text)<4096:
#         await context.bot.send_message(id, text=text, parse_mode=telegram.constants.ParseMode.HTML) 
#     else:
#         chunks = len(text)//4096
#         final = len(text) %4096

#         for i in range(chunks):
#             await context.bot.send_message(id, text=text[i*4096:i+1(4096)], parse_mode=telegram.constants.ParseMode.HTML)
#         await context.bot.send_message(id, text=text[-final:], parse_mode=telegram.constants.ParseMode.HTML) 
                       

async def send_images(title, text, context):
        text, images = parse_img_from_text(text)
        text = markdown_to_html(text)
        caption=f"<b>{title}</b> \n {text}"
        if len(images)==1:
            await context.bot.sendPhoto(chatID, photo=images[0], caption=caption, parse_mode=telegram.constants.ParseMode.HTML)
        else:
            await context.bot.send_media_group(chatID, media=images, caption=caption, parse_mode=telegram.constants.ParseMode.HTML)

async def hot_command(update, context):
    pass
    
application = ApplicationBuilder().token(token).build()
job_queue = application.job_queue
    
hot_handler = CommandHandler('hot', hot_command)
application.add_handler(hot_handler)
job_minute = job_queue.run_repeating(hot, interval=600, first=10)
application.run_polling()