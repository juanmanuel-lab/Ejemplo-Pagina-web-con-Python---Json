from flask import render_template, redirect, url_for, session, flash, request
from app.auth import login_required
from app import app
from app.forms import LoginForm, IngresarPersonalForm
from app.handlers import eliminar_personal, get_personal_por_id, validar_usuario, get_personal, agregar_personal


@app.route('/')  # http://localhost:5000/
@app.route('/index')
@login_required
def index():
    if request.method == 'GET' and request.args.get('borrar'):
        eliminar_personal(request.args.get('borrar'))
        flash('Se ha eliminado el ingreso', 'success')
    return render_template('index.html', titulo="Inicio", personal=get_personal())


@app.route('/ingresar-personal', methods=['GET', 'POST'])
@login_required
def ingresar_personal():
    personal_form = IngresarPersonalForm()
    if personal_form.cancelar.data:  # si se apretó el boton cancelar, personal_form.cancelar.data será True
        return redirect(url_for('index'))
    if personal_form.validate_on_submit():
        datos_nuevos = { 'fecha': personal_form.fecha.data, 'nombre': personal_form.nombre.data, 'apellido': personal_form.apellido.data, 
                         'dni': personal_form.dni.data }
        agregar_personal(datos_nuevos)
        flash('Se ha agregado un nuevo ingreso', 'success')
        return redirect(url_for('index'))
    return render_template('ingresar_personal.html', titulo="Ingresos", personal_form=personal_form)


@app.route('/editar-personal/<int:id_empleado>', methods=['GET', 'POST'])
@login_required
def editar_personal(id_empleado):
    personal_form = IngresarPersonalForm(data=get_personal_por_id(id_empleado))
    if personal_form.cancelar.data:  # si se apretó el boton cancelar, personal_form.cancelar.data será True
        flash('Se ha cancelado la edición del registro, no sé a realizado ninguna modificación.', 'message')
        return redirect(url_for('index'))
    if personal_form.validate_on_submit():
        datos_nuevos = { 'fecha': personal_form.fecha.data, 'nombre': personal_form.nombre.data, 'apellido': personal_form.apellido.data, 
                         'dni': personal_form.dni.data }
        eliminar_personal(id_empleado)  # Eliminamos el empleado antiguo
        agregar_personal(datos_nuevos)  # Agregamos el nuevo empleado
        flash('Se ha editado el ingreso exitosamente', 'success')
        return redirect(url_for('index'))
    return render_template('editar_personal.html', titulo="Ingresos", personal_form=personal_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        usuario = login_form.usuario.data
        password = login_form.password.data
        if validar_usuario(usuario, password):
            session['usuario'] = usuario
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas', 'danger')
    return render_template('login.html', titulo="Login", login_form=login_form)


@app.route('/logout')
@login_required
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

