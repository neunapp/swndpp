(function(){
    "use strict";
    angular.module("DppApp")
        .controller("GuideCtrl", ['$http','$window', GuideCtrl]);

    function GuideCtrl($http, $window){
        var self = this;

        //inicializamos variables globales
        self.choices = [{id:'choice1'},{id:'choice2'}];
        self.buscar = [{id:'buscar1'},{id:'buscar2'}];
        self.cantidad = [{id:0},{id:1}];

        self.msj = "";

        //inicializamos json Guia
        self.guide = {};
        self.guide.asignar = false;


        //inicializamos la lista de proveedores
        $http.get("/api/provider")
          .then(function(response){
              self.providers = response.data;
          }
        );


        //inicializamos la lista de agentes
        self.cagar_agentes = function(){
          $http.get("/api/vendors")
            .then(function(response){
                self.agentes = response.data;
                console.log(self.agentes);
              }
            );
        }


        //inicializamos los valores de dairios desde el servidor
        $http.get("/api/magazine-day/list/")
          .then(function(response){
              self.diarios = response.data;
          }
        );

        //declaramos array que enviaremos para diarios y cantidad
        //metodo que agraga campos dinamicamente
        self.addNewChoice = function(){
            var newItemNo = self.cantidad.length;
            self.choices.push({'id':'choice'+newItemNo});
            self.buscar.push({'id':'buscar'+newItemNo})
            self.cantidad.push({'id':newItemNo});
        };


        //metodo que elimina un formulario
        self.removeChoice = function() {
            var lastItem = self.cantidad.length-1;
            self.choices.splice(lastItem);
            self.buscar.splice(lastItem);
            self.cantidad.splice(lastItem);
        };


        //funcion para enviar datos
        self.enviar = function(){
          if (self.validations()){
            self.msj = "";
            //ingresamos las cantidades no eliminadas al json
            var counts_magazines = [];
            var prod_magazines = []
            for (var i = 0; i < self.cantidad.length; i++) {
                counts_magazines.push(self.count.item[i]);
                prod_magazines.push(self.prod.item[i]);
            }
            //self.guide.provider = self.proveedor
            self.guide.counts = counts_magazines;
            self.guide.prods = prod_magazines;
            //validamos descuento
            if (self.guide.invoce == null) {
              self.guide.invoce=0;
            }
            $http.post("/api/save/guide/add/", self.guide)
                .success(function(res){
                  if (res.id=='0') {
                    console.log('agregado correctamente');
                    window.location.href = '/guia-registrar/';
                  }
                  else {
                    console.log('Erro, no se pudo agregar');
                  }
                  //$location.href
                })
                .error(function(res){
                  self.msj = "ERROR VERIFIQUE QUE LOS DATOS SEAN CORRECTOS";
                  console.log('error no se pudo agregar');
                });
            }
        };

      //========validations===========
      self.validations = function(){
        if ((self.guide.addressee=='')||(self.guide.number=='')||(self.guide.provider=='')||(self.guide.agente=='')) {
          self.msj == 'Por favor ingrese todos los datos'
          return false;
        }
        else {
          self.msj=='';
          return true;
        }
      }
  }
}());
