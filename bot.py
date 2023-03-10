
import telegram
from reddit import RedditScraper, parse_img_from_text, markdown_to_html, check_question
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from const import *
from database import PrevPosts
import time


prev_posts = PrevPosts()

to_update = []

async def hot(context: ContextTypes.DEFAULT_TYPE):
    #creating the temp list to update the db
    

    scraper = RedditScraper()
    hot = scraper.get_hot(num=number_of_posts)
    last_urls = prev_posts.get_last_urls(number_of_posts+40)

    
    time_delay = checking_frequency * 3600 /40
    
    for post in hot:
        
        if (post.url not in last_urls) and (post.url not in to_update):
            
            title = post.title
            text = post.selftext

            if post.stickied or check_question(post):
                continue
            to_update.append(post.url)
            
            if post.is_self:
                if "preview.redd.it" in text:
                    
                    await send_images(title, text, context)
                else:
                    try:
                        await context.bot.send_message(chatID, text=f"<b>{title}</b>\n\n{markdown_to_html(post.selftext)}", parse_mode=telegram.constants.ParseMode.HTML, disable_web_page_preview=True)
                    except:
                        pass


            elif  '.jpg' in post.url or '.png' in post.url or '.gif' in post.url:
                try:
                    await context.bot.sendPhoto(chatID, photo=post.url, caption=f"<b>{title}</b>", parse_mode=telegram.constants.ParseMode.HTML)
                except:
                    pass
            elif 'reddit.com/gallery' in post.url:
                continue
            time.sleep(time_delay)
    
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
            try:
                await context.bot.sendPhoto(chatID, photo=images[0], caption=caption, parse_mode=telegram.constants.ParseMode.HTML)
            except:
                pass
        else:
            try:
                await context.bot.send_media_group(chatID, media=images, caption=caption, parse_mode=telegram.constants.ParseMode.HTML)
            except:
                pass

async def hot_command(update, context):
    pass

# the error handler class tp update the db in a sudde failiure
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    # print("Error")
    prev_posts.insert_urls(to_update)

    

application = ApplicationBuilder().token(token).read_timeout(30).write_timeout(30).build()
job_queue = application.job_queue
    
hot_handler = CommandHandler('hot', hot_command)
application.add_handler(hot_handler)
job_minute = job_queue.run_repeating(hot, interval=checking_frequency * 3600, first=5)
application.add_error_handler(error_handler)
application.run_polling()