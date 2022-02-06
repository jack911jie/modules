import os
import sys
import composing 
import pics_modify
import pics_fill
import re
import json
from PIL import Image,ImageFont,ImageDraw
import logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(funcName)s-%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)


class TxtInGradientBox(composing.TxtFormat,pics_fill.FillGradient,pics_modify.Shape):
    def __init__(self):
        pass

    def draw_rct(self,w=720,h=300,color='#ffffff',radii=0,alpha=1):
        img=Image.new('RGB',(w,h),color)
        if radii>0:
            img=self.circle_corner(img,radii=radii)
        if alpha<1:
            img_bld=Image.new('RGBA',(img.size[0],img.size[1]))
            img=Image.blend(img_bld,img,alpha)
        # img.show()
        return img

    def draw_txt_block(self,txt,wid=600,total_dis=200,y_add=0,color='#ffffff',radii=0,alpha=1,font_size=30,dis_line=30,indent='yes'):
        txt_to_put=self.split_txt_Chn_eng(wid=total_dis,font_size=font_size,txt_input=txt,Indent=indent)
        # print(font_size,dis_line,txt_to_put)
        txts_para_num=txt_to_put['para_num']
        line_para=font_size if dis_line<= font_size else dis_line
        # h_block=int((txts_para_num*font_size+txts_para_num*line_para)*1.3)
        h_block=int((font_size+dis_line)*txts_para_num)
        # print(h_block)
        img=self.draw_rct(w=wid,h=h_block+y_add,color=color,radii=radii,alpha=alpha)
        return img

    def put_txt_to_rct(self,box_wid=300,bg='#ffffff',radii=0,alpha=1,txt='测试',total_dis=250,xy=[10,10],dis_line=30,fill='#333333',font_name='楷体',font_size=30,addSPC='None'):
        if addSPC=='None':
            indent_draw='no'
        else:
            indent_draw='yes'
        img=self.draw_txt_block(txt=txt,wid=box_wid,total_dis=total_dis,y_add=xy[1],color=bg,radii=radii,alpha=alpha,font_size=font_size,dis_line=dis_line,indent=indent_draw)
        draw=ImageDraw.Draw(img)
        self.put_txt_img(draw,tt=txt,total_dis=total_dis,xy=xy,dis_line=dis_line,fill=fill,font_name=font_name,font_size=font_size,addSPC=addSPC)
        return img

    def put_txt_in_grad_rct(self,b_w,colors,gra_direc,radii,alpha,txt_wid,txt_xy,dis_line,txt_input,txt_color,indent,font_name,font_size):       
        
        txt_to_put=self.split_txt_Chn_eng(wid=txt_wid,font_size=font_size,txt_input=txt_input,Indent=indent)
        # print(font_size,dis_line,txt_to_put)
        txts_para_num=txt_to_put['para_num']
        line_para=font_size if dis_line<= font_size else dis_line
        # h_block=int((txts_para_num*font_size+txts_para_num*line_para)*1.3)
        b_h=int((font_size+dis_line)*txts_para_num)
        # print(h_block)
        img=Image.new('RGB',(b_w,b_h),'#ffffff')
        img=self.fill_multi_gradient_rct_rgb(img=img,colors=colors,horizontal=(True,True,True),direction=gra_direc)
        if radii>0:
            img=self.circle_corner(img,radii=radii)
        if alpha<1:
            img_bld=Image.new('RGBA',(img.size[0],img.size[1]))
            img=Image.blend(img_bld,img,alpha)

        draw=ImageDraw.Draw(img)
        if indent=='yes':
            addSPC='yes'
        else:
            addSPC='no'
        self.put_txt_img(draw,tt=txt_input,total_dis=txt_wid,xy=txt_xy,dis_line=dis_line,fill=txt_color,font_name=font_name,font_size=font_size,addSPC=addSPC)

        return img


if __name__=='__main__':
    pic=TxtInGradientBox()
    # rct=pic.draw_rct(w=200,h=700,color='#33ee99',radii=190,alpha=1)
    # rct.show()
    txt=r'观自在菩萨，行深般若波罗蜜多时，照见五蕴皆空，度一切苦厄。舍利子，色不异空，空不异色，色即是空，空即是色，受想行识，亦复如是。舍利子，是诸法空相，不生不灭，不垢不净，不增不减。是故空中无色，无受想行识，无眼耳鼻舌身意，无色声香味触法，无眼界，乃至无意识界，无无明，亦无无明尽，乃至无老死，亦无老死尽。无苦集灭道，无智亦无得。以无所得故。菩提萨埵，依般若波罗蜜多故，心无挂碍。无挂碍故，无有恐怖，远离颠倒梦想，究竟涅盘。三世诸佛，依般若波罗蜜多故，得阿耨多罗三藐三菩提。故知般若波罗蜜多，是大神咒，是大明咒，是无上咒，是无等等咒，能除一切苦，真实不虚。故说般若波罗蜜多咒，即说咒曰：揭谛揭谛，波罗揭谛，波罗僧揭谛，菩提萨婆诃。'
    # rct=pic.draw_txt_block(txt=txt,wid=600,color='#ffffff',radii=0,alpha=1,font_size=30,dis_line=30,indent='yes')
    # rct.show()
    # blk=pic.put_txt_to_img(box_wid=440,bg='#ffffff',radii=0,alpha=1,txt=txt,total_dis=340,xy=(25,30),dis_line=60,fill='#222222',font_name='楷体',font_size=30,addSPC='yes')
    # blk.save('c:/users/jack/desktop/tt.jpg')
    # blk.show()
# self,b_w,colors,gra_direc,radii,alpha,txt_wid,txt_xy,dis_line,txt_input,txt_color,indent,font_name,font_size
    img=pic.put_txt_in_grad_rct(b_w=600,colors=('#fffdee','#fffdee'),gra_direc='vertical',radii=200,alpha=1, 
        txt_wid=450,txt_xy=(25,80),dis_line=50,txt_input=txt,txt_color='#333333',indent='yes',font_name='楷体',font_size=60)
    img.show()



    # tt(200,200,'优设标题',200)