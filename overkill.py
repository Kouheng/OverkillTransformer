import re

""" 
    Overkill transformer
    Read the battle timestamp like 1:30 XXX and subtract it into a overkill time version
    
    Credit by 終將成為你 https://github.com/YungPingXu/pcr-bot/blob/main/main.py
    Rearrange by Kouheng(一杯果汁火) 2020.11.27 """


def check_time(number_line_header):
    """ 檢查是不是合法的時間，合法才會將該行輸入，這裡的運作方式是類filter，符合條件才會回傳
    :param number_line_header 轉換前，軸內開頭的秒數 """

    return (0 <= number_line_header <= 130) and \
           ((number_line_header // 100 == 0 and 59 >= number_line_header % 100 >= 0) or
            (number_line_header // 100 == 1 and 30 >= number_line_header % 100 >= 0))


def transform_time(original_time):  # 轉換秒數
    result = ""
    if original_time < 60:
        if original_time < 10:
            result += "00" + str(original_time)
        else:
            result += "0" + str(original_time)
    else:
        if 60 <= original_time < 70:
            result += str(original_time // 60) + "0" + str(original_time % 60)
        else:
            result += str(original_time // 60) + str(original_time % 60)
    return result


# 給外面指令import用的錯誤訊息
err_msg = ('```因為斜線指令無法換行的緣故，請使用文字指令，使用方式如下:\n'
           '使用 "@花凜 tr [剩餘秒數] [作業內容]"\n'
           '例如: @花凜 tr 30 \n120 果汁 吸毛絨絨的狐狸 \n111 果汁 被甩巴掌的時候\n059 酒鬼```')


def overkill_transformer(time, content):
    """ 將軸內的每一行內容起始秒數扣除掉補償刀消耗的時間並回傳
    :param time 剩餘的補償刀秒數
    :param content 軸的內容，運作上by line """
    if 1 <= time <= 90:
        result_all = ""
        for line in content:
            symbols_filter = line.replace(":", "").replace("\t", "")  # 過濾特殊字元
            match = re.match(r'(\D*)(\d{2,3})((\s*[/~-]\s*)(\d{2,3}))?(.*)?', symbols_filter)  # 擷取時間
            if match:
                content1 = match.group(1)  # 時間前面的文字
                time_range = match.group(3)  # 056~057 這種有範圍的時間
                time1 = int(match.group(2))  # 有範圍的時間 其中的第一個時間
                time2 = 0
                if time_range is not None and match.group(5) is not None:
                    time2 = int(match.group(5))  # 有範圍的時間 其中的第二個時間
                range_content = match.group(4)  # 第一個時間和第二個時間中間的字串
                content2 = match.group(6)  # 時間後面的文字
                if check_time(time1) and ((time_range is None and match.group(5) is None) or (
                        time_range is not None and match.group(5) is not None and check_time(time2))):
                    total_time1 = time1 % 100 + (time1 // 100) * 60  # time1的秒數
                    new_time1 = total_time1 - (90 - time)
                    if new_time1 < 0:  # 如果時間到了 後續的就不要轉換
                        continue  # 迴圈跳到下一個
                    if match.group(5) is None:
                        result_line = content1 + transform_time(new_time1) + content2
                    else:
                        total_time2 = time2 % 100 + time2 // 100 * 60  # time2的秒數
                        new_time2 = total_time2 - (90 - time)
                        result_line = content1 + transform_time(new_time1) + range_content + transform_time(
                            new_time2) + content2
                    result_all += result_line
                else:
                    result_all += line
            else:
                result_all += line
            result_all += "\n"
        return result_all
    else:
        return "您輸入的補償秒數錯誤，秒數必須要在 1～90 之間！"
