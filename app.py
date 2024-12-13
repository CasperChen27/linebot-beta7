from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    FlexMessage,
    FlexBubble,
    FlexImage,
    FlexMessage,
    FlexBox,
    FlexText,
    FlexIcon,
    FlexButton,
    FlexSeparator,
    FlexContainer
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
import os
import json

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_Template_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        # Confirm Template
        if text == 'Confirm':
            confirm_template = ConfirmTemplate(
                text='今天學程式了嗎?',
                actions=[
                    MessageAction(label='是', text='是!'),
                    MessageAction(label='否', text='否!')
                ]
            )
            template_message = TemplateMessage(
                alt_text='Confirm alt text',
                template=confirm_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )
        # Buttons Template
        elif text == 'Buttons':
            url = request.url_root + 'static/Guns&Roses.jpg'
            url = url.replace("https", "http")
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            buttons_template = ButtonsTemplate(
                thumbnail_image_url=url,
                title='槍與玫瑰社群',
                text='關注我們的社交帳號以獲得最新資訊!',
                actions=[
                    URIAction(label='fb連結', uri='https://www.facebook.com/GunsNRosesBar/?ref=bookmarks&_rdr'),
                    URIAction(label='instagram連結', uri='https://www.instagram.com/guns__roses_bar/'),
                    URIAction(label='店家地址', uri='https://www.google.com/maps?q=621%E5%98%89%E7%BE%A9%E7%B8%A3%E6%B0%91%E9%9B%84%E9%84%89%E8%A3%95%E8%BE%B2%E4%B8%80%E8%A1%9723%E8%99%9F%E6%A7%8D%E8%88%87%E7%8E%AB%E7%91%B0&ftid=0x346ebe50129cbe03:0xe69959cc7d9c99c0&entry=gps&lucs=,94246480,94242505,94224825,94227247,94227248,47071704,47069508,94218641,94228354,94233079,94203019,47084304,94208458,94208447&g_ep=CAISEjI0LjQ3LjMuNjk4NTMxOTU1MBgAIJ6dCip-LDk0MjQ2NDgwLDk0MjQyNTA1LDk0MjI0ODI1LDk0MjI3MjQ3LDk0MjI3MjQ4LDQ3MDcxNzA0LDQ3MDY5NTA4LDk0MjE4NjQxLDk0MjI4MzU0LDk0MjMzMDc5LDk0MjAzMDE5LDQ3MDg0MzA0LDk0MjA4NDU4LDk0MjA4NDQ3QgJUVw%3D%3D&g_st=com.google.maps.preview.copy'),
                    # PostbackAction(label='回傳值', data='ping', displayText='傳了'),
                    # MessageAction(label='傳"哈囉"', text='哈囉'),
                    # DatetimePickerAction(label="選擇時間", data="時間", mode="datetime"),
                    # CameraAction(label='拍照'),
                    # CameraRollAction(label='選擇相片'),
                    # LocationAction(label='選擇位置')
                ]
            )
            template_message = TemplateMessage(
                alt_text="This is a buttons template",
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )
        # ImageCarousel Template
        elif text == 'ImageCarousel':
            url = request.url_root + 'static/'
            url = url.replace("https", "http")
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            image_carousel_template = ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=url+'guns&rosesfb.png',
                        action=URIAction(
                            label='造訪我們的FB',
                            uri='https://www.facebook.com/GunsNRosesBar/?ref=bookmarks&_rdr'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=url+'guns&rosesig.png',
                        action=URIAction(
                            label='造訪我們的IG',
                            uri='https://www.instagram.com/guns__roses_bar/'
                        )
                    ),
                    #ImageCarouselColumn(
                     #   image_url=url+'youtube.png',
                      #  action=URIAction(
                       #     label='造訪YT',
                        #    uri='https://www.youtube.com/@bigdatantue'
                       # )
                    #),
                ]
            )

            image_carousel_message = TemplateMessage(
                alt_text='傳送一則訊息',
                template=image_carousel_template
            )

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[image_carousel_message]
                )
            )
            
#def handle_flex_message(event):
   # text = event.message.text
   # with ApiClient(configuration) as api_client:
   #     line_bot_api = MessagingApi(api_client)

        if text == 'flex message':
            line_flex_json = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://lh5.googleusercontent.com/p/AF1QipPW5OoPSzzo4XloRdjLqKxDWfDQXsFEbtDFla3p=w408-h544-k-no",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Brown Cafe",
        "weight": "bold",
        "size": "xl",
        "contents": [
          {
            "type": "span",
            "text": "槍與玫瑰"
          }
        ]
      },
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "icon",
            "size": "sm",
            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
          },
          {
            "type": "icon",
            "size": "sm",
            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
          },
          {
            "type": "icon",
            "size": "sm",
            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
          },
          {
            "type": "icon",
            "size": "sm",
            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
          },
          {
            "type": "icon",
            "size": "sm",
            "url": "https://i.ibb.co/W3DSvJD/halfstar.png"
          },
          {
            "type": "text",
            "text": "4.4",
            "size": "sm",
            "color": "#999999",
            "margin": "md",
            "flex": 0
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "地址",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "621嘉義縣民雄鄉裕農一街23號",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "營業時間",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 3
              },
              {
                "type": "text",
                "text": "21:00 - 02:00",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 7
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "查看位址",
          "uri": "https://www.google.com/maps/place/%E6%A7%8D%E8%88%87%E7%8E%AB%E7%91%B0/@23.557281,120.4707417,17z/data=!3m1!4b1!4m6!3m5!1s0x346ebe50129cbe03:0xe69959cc7d9c99c0!8m2!3d23.557281!4d120.4707417!16s%2Fg%2F1pp2vgyfs?entry=ttu&g_ep=EgoyMDI0MTIxMC4wIKXMDSoASAFQAw%3D%3D"
        }
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "margin": "sm"
      }
    ],
    "flex": 0
  }
}
            
            line_flex_str = json.dumps(line_flex_json)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text='詳細說明', contents=FlexContainer.from_json(line_flex_str))]
                )
            )   

if __name__ == "__main__":
    app.run()