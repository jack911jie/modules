import os
import re
import json
from PIL import Image,ImageFont,ImageDraw
import logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(funcName)s-%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)

class TxtFormat:
    def char_len(self,txt):
        len_s=len(txt)
        len_u=len(txt.encode('utf-8'))
        ziShu_z=(len_u-len_s)/2
        ziShu_e=len_s-ziShu_z
        total=ziShu_z+ziShu_e*0.5
        return total

    def fonts(self,font_name,font_size):
        with open(os.path.join(os.path.dirname(__file__),'fonts_list.config'),'r',encoding='utf-8') as f:
            lines=f.readlines()
            _line=''
            for line in lines:
                newLine=line.strip('\n')
                _line=_line+newLine
            fontList=json.loads(_line)
        

        return ImageFont.truetype(fontList[font_name],font_size)

    def split_txt_Chn_eng(self,wid,font_size,txt_input,Indent='no'):
        
        def put_words(txts,zi_per_line):    
            txtGrp=[]
            wd_lng=0
            pre_txt=''
            for c,t in enumerate(txts):
                if res.match(t):
                    if wd_lng+1>zi_per_line:
                        txtGrp.append(pre_txt)
                        pre_txt=t
                        wd_lng=1
                    else:
                        pre_txt=pre_txt+t
                        wd_lng=wd_lng+1
                else:
                    if t in ['”','’','，','。','！','：','；','.',',','!','”。','”，']:
                        pre_txt=pre_txt+' '+t
                        wd_lng=wd_lng+self.char_len(t)
                    else:    
                        if wd_lng+self.char_len(t)>zi_per_line: #先判断是这个英文单词+原有拼接的字符串长度是否>每行字符数
                            txtGrp.append(pre_txt) #大于，则保持原有的拼接字符串，不再加入该英文单词
                            pre_txt=' '+t #新的英文单词另起一行
                            wd_lng=self.char_len(t) #拼接字符串长度清零重计
                        else:                    
                            pre_txt=pre_txt+' '+t
                            wd_lng=wd_lng+self.char_len(t)

                if wd_lng>zi_per_line:
                    wd_lng=0                
                    txtGrp.append(pre_txt)
                    pre_txt=''                
                else:
                    if c==len(txts)-1:
                        wd_lng=0                
                        txtGrp.append(pre_txt)
                        pre_txt='' 
                        
                    
            logging.info(txtGrp)
            return txtGrp
        
        txts=txt_input.splitlines()
        logging.info(txts)    
        
        if Indent=='yes':
            for i,t in enumerate(txts):
                txts[i]=chr(12288)+chr(12288)+t
        
        # print('composing line 82:', txts)
        
        res = re.compile(r'([\u4e00-\u9fa5])')   
        singleTxts=[]
        for t in txts:
            _t=res.split(t)
            _t_no_empty=list(filter(None,_t))      
            singleTxts.append(_t_no_empty)        
        
        split_txt=[]
        for singleTxt in singleTxts:
            grp=[]
            for st in singleTxt:
                if res.match(st):
                    grp.append(st)
                else:
                    grp.extend(st.split(' '))
            split_txt.append(grp)
            
        logging.info(split_txt)
            
        
        total_num=0
        for r in split_txt:
            total_num=total_num+len(r)
            
        zi_per_line=int(wid//font_size)
            
        outTxt=[]
        for r,split_t in enumerate(split_txt):
            outTxt.append(put_words(split_t,zi_per_line))
            
        para_num=0
        for tt in outTxt:
            for t in tt:
                para_num+=1
    
        return  {'txt':outTxt,'para_num':para_num}

    def put_txt_img(self,draw,tt,total_dis,xy,dis_line,fill,font_name,font_size,addSPC='no'):
            
        fontInput=self.fonts(font_name,font_size)            
        if addSPC=='yes': 
            Indent='yes'
        else:
            Indent='no'
            
        # txt=self.split_txt(total_dis,font_size,t,Indent='no')
        txt=self.split_txt_Chn_eng(total_dis,font_size,tt,Indent=Indent)
        # font_sig = self.fonts('丁永康硬笔楷书',40)
        num=len(txt)   
        # draw=ImageDraw.Draw(img)

        logging.info(txt)
        n=0
        for t in txt['txt']:              
            m=0
            for tt in t:                  
                x,y=xy[0],xy[1]+(font_size+dis_line)*n
                if addSPC=='add_2spaces':   #首行缩进
                    if m==0:    
                        # tt='  '+tt #首先前面加上两个空格
                        logging.info('字数：'+str(len(tt))+'，坐标：'+str(x)+','+str(y))
                        logging.info(tt)
                        draw.text((x+font_size*0.2,y), tt, fill = fill,font=fontInput) 
                    else:                       
                        logging.info('字数：'+str(len(tt))+'，坐标：'+str(x)+','+str(y))
                        logging.info(tt)
                        draw.text((x,y), tt, fill = fill,font=fontInput)  
                else:
                    # logging.info('字数：'+str(len(tt))+'，坐标：'+str(x)+','+str(y))
                    # logging.info(tt)
                    draw.text((x,y), tt, fill = fill,font=fontInput)  

                m+=1
                n+=1

    def char_len(self,txt):
        len_s=len(txt)
        len_u=len(txt.encode('utf-8'))
        ziShu_z=(len_u-len_s)/2
        ziShu_e=len_s-ziShu_z
        total=ziShu_z+ziShu_e*0.5    
        return total