import smtplib 
import email.message

def enviar_email(dados):
    try:
        corpo_email = """
        Olá Vinicius, venho trazer os dados de clima de hoje!
        Segue meu email automatico
        """
        msg = email.message.Message()
        msg['Subject'] = "Assunto"
        msg['From'] = 'noreply.ecosystemcall@gmail.com'
        msg['To'] = 'noreply.ecosystemcall@gmail.com'
        password = 'ugtfjofbzmglyssy'
        msg.add_header('Contect-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = smtplib.SMTP('smtp.gmail.com:587')
        s.starttls()
        s.login(msg['From'],password)
        s.sendmail(msg['From'],[msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado')
    except Exception as e:
        print(e)
if __name__ == "__main__":
    enviar_email()
