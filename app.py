from datetime import date,datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request,redirect,render_template,url_for
from flask.ext.security import Security, SQLAlchemyUserDatastore,UserMixin, RoleMixin, login_required
from flask import g
from flask.json import jsonify
from flask import flash


app =Flask(__name__)
db =SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost/flaskistekdb'
app.debug=True
#"'postgresql://username:password@localhost/databasename'
app.secret_key = 'super secret key'

class Birim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    birim_adi = db.Column(db.String(255))

    def __init__(self,birim_adi):
            self.birim_adi=birim_adi

    def __repr__(self):
            return '<Birim %r>' % self.birim_adi


class IstekSahibi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    birim_id =db.Column(db.Integer, db.ForeignKey('birim.id'))
    adi=db.Column(db.String(255))
    soyadi=db.Column(db.String(255))

    def __init__(self,birim_id,adi,soyadi):
            self.birim_id=birim_id
            self.adi=adi
            self.soyadi=soyadi

    def __repr__(self):
            return '<IstekSahibi %r>' % self.adi

class VeriFormat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adi=db.Column(db.String(255))
    kodu=db.Column(db.String(255))

    def __init__(self,adi,kodu):
            self.adi=adi
            self.kodu=kodu

    def __repr__(self):
            return '<VeriFormat %r>' % self.adi


class VeriKoordinat(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    adi=db.Column(db.String(255))
    kodu=db.Column(db.String(255))

    def __init__(self,id,adi,kodu):
            self.id=id
            self.adi=adi
            self.kodu=kodu

    def __repr__(self):
            return '<VeriKoordinat %r>' % self.adi



class Istek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adi=db.Column(db.String(255))
    isteksahibi_id = db.Column(db.Integer, db.ForeignKey('istek_sahibi.id'))
    veriformat_id= db.Column(db.Integer, db.ForeignKey('veri_format.id'))
    verikoordinat_id= db.Column(db.Integer, db.ForeignKey('veri_koordinat.id'))
    istektalep_tarihi=db.Column(db.DateTime)
    istekteslim_tarihi=db.Column(db.DateTime)
    istekaciklama=db.Column(db.Text)
    istekveriyolu=db.Column(db.Text)
    def __init__(self,adi,isteksahibi_id,veriformat_id,verikoordinat_id,istektalep_tarihi,istekteslim_tarihi,istekaciklama=None,istekveriyolu=None,):
            self.adi=adi
            self.isteksahibi_id=isteksahibi_id
            self.veriformat_id=veriformat_id
            if istektalep_tarihi is '':
                #istektalep_tarihi = date.today()
                istektalep_tarihi = None
            self.istektalep_tarihi=istektalep_tarihi
            if istekteslim_tarihi is '':
                istekteslim_tarihi = None
            self.istekteslim_tarihi=istekteslim_tarihi
            self.istekaciklama=istekaciklama
            self.istekveriyolu=istekveriyolu
            self.verikoordinat_id=verikoordinat_id

    def __repr__(self):
            return '<Istek %r>' % self.birim_adi

###http://stackoverflow.com/questions/23557063/passing-value-from-a-drop-down-menu-to-a-flask-template


##Data Entery in Birim List
@app.route('/')
def index():
      birim =Birim.query.all()
      istekSahibi=IstekSahibi.query.all()
      istek=Istek.query.all()
      veriFormat=VeriFormat.query.all()
      veriKoordinat=VeriKoordinat.query.all()

      return render_template('index.html',birim=birim,istekSahibi=istekSahibi,istek=istek,veriFormat=veriFormat,veriKoordinat=veriKoordinat)

# @app.route('/profile/<id>')
# def profile(id):
#      birim =Birim.query.all()
#      return render_template('birimprofile.html',birim=birim)

#
# @app.route('/edit_birim/<int:id>',methods=['GET','POST'])
# def edit_birim(id):
#     birimwithid = db.session.query(Birim).filter(Birim.id==id).first()
#
#     if request.method == 'POST':
#         adi = request.form['birimwithidadi']
#         print("veri geldi", adi)
#         birimwithid.birim_adi = adi
#         db.session.commit()
#
#         return redirect(url_for('index', birimwithid=birimwithid))
#     else:
#         return render_template('index.html')

@app.route('/edit_birim/<id>',methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def edit_birim(id):
    birim=Birim.query.all()
    birimSelectedWithID=db.session.query(Birim).filter(Birim.id==id).first()
    #birimtest=str(db.session.query(Birim).filter(Birim.id == id).first())
    #print (birimtest)
    if request.method == 'POST':
          adi = request.form['birimwithidadi']
          birimSelectedWithID.birim_adi = adi
          db.session.commit()
          return render_template('birimprofile.html',birim=birim,birimSelectedWithID=birimSelectedWithID,id = id)
    else:
        return render_template('birimprofile.html',birim=birim,birimSelectedWithID=birimSelectedWithID,id = id)

@app.route('/delete_birim/<id>',methods = ['POST'])
def delete_birim(id):
    if request.method == 'POST':
         Birim.query.filter(Birim.id == id).delete()
         db.session.commit()
         flash('Entry was deleted')
         return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/edit_isteksahibi/<id>',methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def edit_isteksahibi(id):
    birim=Birim.query.all() #birim secimi için
    isteksahibi=IstekSahibi.query.all()
    istekSelectedWithID=db.session.query(Istek).filter(Istek.id==id).first()
    #birimtest=str(db.session.query(Birim).filter(Birim.id == id).first())
    #print (birimtest)
    if request.method == 'POST':
          adi = request.form['istekSelectedWithID_adi']
          istekSelectedWithID.adi = adi
          isteksahibi_id = request.form['istekSelectedWithID_isteksahibi_id']
          istekSelectedWithID.isteksahibi_id = isteksahibi_id
          veriformat_id = request.form['istekSelectedWithID_veriformat_id']
          istekSelectedWithID.veriformat_id = veriformat_id
          verikoordinat_id = request.form['istekSelectedWithID_verikoordinat_id']
          istekSelectedWithID.verikoordinat_id = verikoordinat_id
          istektalep_tarihi = request.form['istekSelectedWithID_istektalep_tarihi']
          istekSelectedWithID.istektalep_tarihi = istektalep_tarihi
          istekteslim_tarihi = request.form['istekSelectedWithID_istekteslim_tarihi']
          istekSelectedWithID.istekteslim_tarihi = istekteslim_tarihi
          istekaciklama = request.form['istekSelectedWithID_istekaciklama']
          istekSelectedWithID.istekaciklama = istekaciklama
          istekveriyolu = request.form['istekSelectedWithID_istekveriyolu']
          istekSelectedWithID.istekveriyolu = istekveriyolu
          db.session.commit()
          return render_template('isteksahibiprofile.html',birim=birim,isteksahibi=isteksahibi,istekSelectedWithID=istekSelectedWithID,id = id)
    else:
        return render_template('isteksahibiprofile.html',birim=birim,isteksahibi=isteksahibi,istekSelectedWithID=istekSelectedWithID,id = id)


@app.route('/delete_isteksahibi/<id>',methods = ['POST'])
def delete_isteksahibi(id):
    if request.method == 'POST':
         IstekSahibi.query.filter(IstekSahibi.id == id).delete()
         db.session.commit()
         flash('Entry was deleted')
         return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))



@app.route('/edit_istek/<id>',methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def edit_istek(id):
    birim=Birim.query.all() #birim secimi için
    isteksahibi=IstekSahibi.query.all()
    istekSahibiSelectedWithID=db.session.query(IstekSahibi).filter(IstekSahibi.id==id).first()
    #birimtest=str(db.session.query(Birim).filter(Birim.id == id).first())
    #print (birimtest)
    if request.method == 'POST':
          birim_id = request.form['istekSahibiSelectedWithID_birim_id']
          istekSahibiSelectedWithID.birim_id = birim_id
          adi = request.form['istekSahibiSelectedWithID_adi']
          istekSahibiSelectedWithID.adi = adi
          soyadi = request.form['istekSahibiSelectedWithID_soyadi']
          istekSahibiSelectedWithID.soyadi = soyadi
          db.session.commit()
          return render_template('isteksahibiprofile.html',birim=birim,isteksahibi=isteksahibi,istekSahibiSelectedWithID=istekSahibiSelectedWithID,id = id)
    else:
        return render_template('isteksahibiprofile.html',birim=birim,isteksahibi=isteksahibi,istekSahibiSelectedWithID=istekSahibiSelectedWithID,id = id)


@app.route('/delete_istek/<id>',methods = ['POST'])
def delete_istek(id):
    if request.method == 'POST':
         Istek.query.filter(Istek.id == id).delete()
         db.session.commit()
         flash('Entry was deleted')
         return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))





@app.route('/post_isteksahibi', methods=['POST'])
def post_isteksahibi():
     istekSahibi=IstekSahibi(request.form['isteksahibi_birim_id'],request.form['isteksahibi_adi'],request.form['isteksahibi_soyadi'])
     db.session.add(istekSahibi)
     db.session.commit()
     return redirect(url_for('index'))

@app.route('/post_birim', methods=['POST'])
def post_birim():
     birim=Birim(request.form['birim_adi'])
     db.session.add(birim)
     db.session.commit()
     return redirect(url_for('index'))

@app.route('/post_veriformat', methods=['POST'])
def post_veriformat():
     veriformat=VeriFormat(request.form['veriformat_adi'],request.form['veriformat_kodu'])
     db.session.add(veriformat)
     db.session.commit()
     return redirect(url_for('index'))


@app.route('/post_verikoordinat', methods=['POST'])
def post_verikoordinat():
     verikoordinat=VeriKoordinat(request.form['verikoordinat_id'], request.form['verikoordinat_adi'],request.form['verikoordinat_kodu'])
     db.session.add(verikoordinat)
     db.session.commit()
     return redirect(url_for('index'))

@app.route('/post_istek', methods=['POST'])
def post_istek():
     istek=Istek(request.form['istek_adi'],request.form['isteksahibi_id'],request.form['veriformat_id'],request.form['verikoordinat_id'],request.form['istektalep_tarihi'],request.form['istekteslim_tarihi'],request.form['istekaciklama'],request.form['istekveriyolu'])
     db.session.add(istek)
     db.session.commit()
     return redirect(url_for('index'))

if __name__=="__main__":
    app.run()
