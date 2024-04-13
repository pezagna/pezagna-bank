from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Variáveis globais para manter o estado do sistema bancário
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

@app.route("/", methods=["GET", "POST"])
def home():
    global saldo, extrato, numero_saques

    if request.method == "POST":
        # Obter a opção selecionada
        opcao = request.form.get("opcao")
        
        # Realizar operações com base na opção selecionada
        if opcao == "d":
            valor = float(request.form.get("valor"))
            if valor > 0:
                saldo += valor
                extrato += f"Depósito: R$ {valor:.2f}\n"
            else:
                return render_template("index.html", error="O valor informado é inválido.", saldo=saldo, extrato=extrato)

        elif opcao == "s":
            valor = float(request.form.get("valor"))
            excedeu_saldo = valor > saldo
            excedeu_limite = valor > limite
            excedeu_saques = numero_saques >= LIMITE_SAQUES

            if excedeu_saldo:
                return render_template("index.html", error="Você não tem saldo suficiente.", saldo=saldo, extrato=extrato)
            elif excedeu_limite:
                return render_template("index.html", error="O valor do saque excede o limite.", saldo=saldo, extrato=extrato)
            elif excedeu_saques:
                return render_template("index.html", error="Número máximo de saques excedido.", saldo=saldo, extrato=extrato)
            elif valor > 0:
                saldo -= valor
                extrato += f"Saque: R$ {valor:.2f}\n"
                numero_saques += 1
            else:
                return render_template("index.html", error="O valor informado é inválido.", saldo=saldo, extrato=extrato)

        elif opcao == "e":
            return render_template("index.html", extrato=extrato, saldo=saldo)

        return redirect(url_for("home"))

    return render_template("index.html", saldo=saldo, extrato=extrato)

if __name__ == "__main__":
    app.run(debug=True)
