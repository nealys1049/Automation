# !/usr/bin/env python
# -*-coding:utf-8 -*-

import calendar
import poplib
import re
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


class Email:
    def __init__(self, email, password, pop3_server='pop.chinatelecom.cn'):
        # 连接到POP3服务器:
        self.server = poplib.POP3_SSL(pop3_server)
        # 可以打开或关闭调试信息:
        # self.server.set_debuglevel(1)
        # 可选:打印POP3服务器的欢迎文字:
        # print(server.getwelcome().decode('utf-8'))

        # 身份认证:
        self.server.user(email)
        self.server.pass_(password)

        # stat()返回邮件数量和占用空间:
        # print('Messages: %s. Size: %s' % server.stat())
        # list()返回所有邮件的编号:
        resp, mails, octets = self.server.list()
        # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
        # print(mails)

        # 获取最新一封邮件, 注意索引号从1开始:
        index = len(mails)
        resp, lines, octets = self.server.retr(index)
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        self.msg_content = b'\r\n'.join(lines).decode('utf-8')

        # print(get_date)
        # 稍后解析出邮件:
        self.msg = Parser().parsestr(self.msg_content)
        # 关闭连接:
        self.server.quit()
        self.body = ''
        self.header_dict = {}

    def get_email_time(self):
        get_date = re.search(r'Date:\s([A-Za-z]{1,3}),\s([0-9]{1,2})\s([A-Za-z]{1,3})\s([0-9]{1,4})\s([0-9]{1,2}):',
                             self.msg_content)
        return '{}-{}-{}'.format(get_date.group(4),
                                 str(list(calendar.month_abbr).index(get_date.group(3))).zfill(2),
                                 str(get_date.group(2)).zfill(2))

    def get_header_info(self, msg, indent=0):
        self.msg = msg
        if indent == 0:
            for header in ['From', 'To', 'Subject']:
                value = self.msg.get(header, '')
                if value:
                    if header == 'Subject':
                        value = self.decode_str(value)
                    else:
                        hdr, addr = parseaddr(value)
                        name = self.decode_str(hdr)
                        value = u'%s <%s>' % (name, addr)
                self.header_dict[header] = value
                # print('%s%s: %s' % ('  ' * indent, header, value))
            return self.header_dict

    def get_body_info(self, msg, indent=0):
        self.msg = msg
        if not self.msg.is_multipart():
            content_type = self.msg.get_content_type()
            if content_type == 'text/plain':
                content = self.msg.get_payload(decode=True)
                charset = self.guess_charset(self.msg)
                if charset:
                    content = content.decode(charset)
                self.body = content
        else:
            parts = self.msg.get_payload()
            for n, part in enumerate(parts):
                self.get_body_info(part, indent=indent + 1)
        return self.body

    @staticmethod
    def decode_str(s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    @staticmethod
    def guess_charset(msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

txt = '转集团大客户工单系统(2301090354117194), 客户名称：赵忠磊, 故障现象描述：2023-1-9 P4 杭州 计算节点扩容 HZ-AZ01-POD07-S3-Normal04-CNA179 ZJKQ01-S3E-K04-SEV-RH128-1U09 计算节点 HZ-AZ01-POD07-S3-Normal04 1288H V5 2102312CLP10K3000077 10.190.165.144 10.254.236.194 02311HAP 硬盘 下电核对SN和BOM更换系统盘，SN：WFJ1L2NS'


def get_ipandport(txt):
    # 默认网页内的IP地址位于端口号之前，并且中间至少隔了一个非数字的字符串
    # (?:((?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5]))  用于匹配IP地址
    # (6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9])    用于匹配端口号 注意端口号匹配规则应从大到校排序
    # 使用 ([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-5]{2}[0-3][0-5]) 替换即可观察到原因。
    # 使用\D+?匹配IP地址与端口号中间至少隔了一个非数字的字符串
    p = r'(?:((?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5]))\D+?(6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9]))'
    iplist = re.findall(p, txt)
    for each in iplist:
        print(each)

if __name__ == '__main__':
    ema = Email('yus6@chinatelecom.cn', '3kD)qVr7%m5BYA*k')
    a = ema.get_header_info(msg=ema.msg)
    b = ema.get_body_info(msg=ema.msg)
    c = ema.get_email_time()
    print(a)
    print(b)
    print(c)
    get_ipandport(b)

