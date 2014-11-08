(function() {
'use strict;'

UserCtrl = function($http, $scope) {
    var user
    this.getCompanies = function(){
        $http.get('../api?q=companies')
            .then(function(response) {
                $scope.data = response.data
            })
    }
    this.getUser = function(email){
        $http.get('../api?q=user&user=' + email)
            .then(function(response) {
                $scope.user = response.data
            })
    }
    this.init = function() {
        user = document.getElementById('username')
        if (user != null) {
            this.user = this.getUser(user.text)
        }
    }
    this.getCompanies()
}

MainCtrl = function($http, $scope) {
    this.getContacts = function(email){
        $http.get('../api?q=contacts&user=' + email)
            .then(function(response) {
                $scope.data = response.data
            })
    }
    this.getInbox = function(email){
        $http.get('../api?q=received&user=' + email)
            .then(function(response) {
                $scope.data = response.data
            })
    }
    this.getSent = function(email){
        $http.get('../api?q=sent&user=' + email)
            .then(function(response) {
                $scope.data = response.data
            })
    }
}

MsgCtrl = function($http, $scope) {
  this.send = function(){
    data = {
            'user': this.user,
            'mobile_number': this.number.toString(),
            'message': this.message,
            'request_cost': 'P2.50',
        }
    $http.post('/api', data)
        //.then(console.log('Success'))
    this.number = this.message = ''
  }
}

angular.module('app', [
])
.controller('UserCtrl', [
    '$http',
    '$scope',
    UserCtrl
])
.controller('MainCtrl', [
    '$http',
    '$scope',
    MainCtrl
])
.controller('MsgCtrl', [
    '$http',
    '$scope',
    MsgCtrl
])
.filter("asDate", function () {
    return function (input) {
        d = new Date(0)
        return d.setUTCSeconds(input)
    }
})
})();