import math
import os
import time
import json
from main.plugins.helpers import TimeFormatter, humanbytes

#------
FINISHED_PROGRESS_STR = "▰"
UN_FINISHED_PROGRESS_STR = "▱"
DOWNLOAD_LOCATION = "/app"


async def progress_for_pyrogram(
    current,
    total,
    bot,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        status = f"{DOWNLOAD_LOCATION}/status.json"
        if os.path.exists(status):
            with open(status, 'r+') as f:
                statusMsg = json.load(f)
                if not statusMsg["running"]:
                    bot.stop_transmission()
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "**[{0}{1}]**\n".format(
            ''.join(
                    FINISHED_PROGRESS_STR
                    for _ in range(math.floor(percentage / 14))
            ),
            ''.join(
                    UN_FINISHED_PROGRESS_STR
                    for _ in range(14 - math.floor(percentage / 14))
            )

        tmp = progress + "├ 𝙎𝙞𝙯𝙚: {0} / {1}\n├ 𝙎𝙥𝙚𝙚𝙙: {2}/s\n├ 𝙀𝙏𝘼: {3}\n╰─⌈ 𝘽𝙤𝙩 𝙢𝙖𝙙𝙚 𝙗𝙮 𝙏𝙀𝘼𝙈 𝙎𝙋𝙔 ⌋──╯".format(str(variable_0), str(variable_1), str(variable_2), str(variable_3))

            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            text = f"{ud_type}\n {tmp}"
            if message.text != text or message.caption != text:
                if not message.photo:
                    await message.edit_text(text=f"{ud_type}\n {tmp}")

                else:
                    await message.edit_caption(caption=f"{ud_type}\n {tmp}")
        except:
            pass


