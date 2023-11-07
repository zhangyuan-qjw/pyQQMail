# mail项目邮件发送需要的格式

>主题：章远
>
>2921572176@qq.comT0219U12D0

**该项目不需要写具体邮件，只需要固定的模板要求即可，全由AI生成，所以局限性很多，仅个人使用！**

## T

- 1229表示十二月二十九

- 0219表示二月一十九

  

## U

- 00表示零点【或者24】
- 12中午12点

## D

- 0表示每年
- 1表示一年

## 数据库字段

```sql
CREATE DATABASE mail;

CREATE TABLE taskMail (
  Date VARCHAR(20),
  Time VARCHAR(20), 
  Sendto VARCHAR(40),
  Template VARCHAR(20),
  Subject VARCHAR(40),
  Num INT
);
```

