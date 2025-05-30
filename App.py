from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'segredo123'  # necessário para flash messages

# Dados simulados (em memória)
profissionais = ['Ana', 'Bruno', 'Carla']
agendamentos = []  # lista de dicts com agendamentos

@app.route('/')
def index():
    return render_template('index.html', profissionais=profissionais, agendamentos=agendamentos)

@app.route('/cliente', methods=['GET', 'POST'])
def cliente():
    if request.method == 'POST':
        cliente_nome = request.form['cliente_nome']
        profissional = request.form['profissional']
        data_hora = request.form['data_hora']  # formato: 'YYYY-MM-DDTHH:MM'

        # Verificar conflito de horário para o profissional
        for ag in agendamentos:
            if ag['profissional'] == profissional and ag['data_hora'] == data_hora:
                flash(f'Conflito: O profissional {profissional} já tem um agendamento nesse horário.', 'error')
                return redirect(url_for('cliente'))

        agendamentos.append({
            'tipo': 'Cliente',
            'cliente_nome': cliente_nome,
            'profissional': profissional,
            'data_hora': data_hora
        })
        flash('Agendamento realizado com sucesso!', 'success')
        return redirect(url_for('cliente'))

    return render_template('cliente.html', profissionais=profissionais, agendamentos=agendamentos)

@app.route('/profissional', methods=['GET', 'POST'])
def profissional():
    if request.method == 'POST':
        prof_nome = request.form['prof_nome']
        data_hora = request.form['data_hora']

        # Verificar conflito de horário para o profissional
        for ag in agendamentos:
            if ag['profissional'] == prof_nome and ag['data_hora'] == data_hora:
                flash('Conflito: Você já tem um agendamento nesse horário.', 'error')
                return redirect(url_for('profissional'))

        agendamentos.append({
            'tipo': 'Profissional',
            'profissional': prof_nome,
            'data_hora': data_hora
        })
        flash('Agendamento registrado com sucesso!', 'success')
        return redirect(url_for('profissional'))

    return render_template('profissional.html', profissionais=profissionais, agendamentos=agendamentos)

if __name__ == '__main__':
    app.run(debug=True)
