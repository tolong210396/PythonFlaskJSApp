angular.module('myApp', [])
            .controller('HomeCtrl', function($scope, $http) {

                $scope.info = {};

                $scope.showAdd = true;

                $scope.searchName   = '';

                $scope.sortType     = 'account_number';
                
                $scope.sortReverse  = false;

                $scope.showlist = function() {
                    $http({
                        method: 'POST',
                        url: '/getaccount',

                    }).then(function(response) {
                        $scope.listdb = response.data;
                        console.log('mm', $scope.listdb);
                    }, function(error) {
                    console.log(error);
                    });
                }

                $scope.show_one = function(id) {
                    $scope.info.id = id;

                    $scope.showAdd = false;

                    $http({
                        method: 'POST',
                        url: '/getaccount_one',
                        data: {id:$scope.info.id}
                    }).then(function(response) {
                        $scope.account = response.data;
                        console.log('mm', $scope.account);
                    }, function(error) {
                    console.log(error);
                    });
                }

                $scope.addaccount = function(){
                    $http({
                        method: 'POST',
                        url: '/addaccount',
                        data: {info:$scope.info}
                    }).then(function(response) {
                        $scope.showlist();
                        $scope.info = {}
                    }, function(error) {
                    console.log(error);
                    });
                }

                $scope.editAccount = function(id){
                    $scope.info.id = id;
                    
                    $scope.showAdd = false;
                    
                    $http({
                        method: 'POST',
                        url: '/getaccount_one',
                        data: {id:$scope.info.id}
                    }).then(function(response) {
                        console.log(response);
                        $scope.info = response.data;
                    }, function(error) {
                        console.log(error);
                    });
                }
                
                $scope.updateAccount= function(){
                
                    $http({
                        method: 'POST',
                        url: '/updateAccount',
                        data: {info:$scope.info}
                    }).then(function(response) {
                        //console.log(response.data);
                        $scope.showlist();
                        $scope.info = {}
                    }, function(error) {
                        console.log(error);
                    });
                }

                $scope.Delete_account = function(id){
                    $scope.deleteAccountId = id;
                    $('#deleteConfirm').modal('show');
                }

                $scope.deleteAccount = function(){
                    
                    $http({
                        method: 'POST',
                        url: '/deleteAccount',
                        data: {id:$scope.deleteAccountId}
                    }).then(function(response) {
                        console.log(response.data);
                        $scope.deleteAccountId = '';
                        $scope.showlist();
                        $('#deleteConfirm').modal('hide')
                    }, function(error) {
                        console.log(error);
                    });
                }

                $scope.showlist();
            })
