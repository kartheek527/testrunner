angular
      .module('snapshot', ['ngMaterial', 'ngMessages', 'md.data.table'])
      .config(function($interpolateProvider, $mdThemingProvider) {
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
        $mdThemingProvider.theme('default')
          .primaryPalette('blue');
      })
      .controller('cardController', cardController);

    function cardController($scope, $mdToast, $http) {

      $scope.selected = [];
      $scope.client = {}
      $scope.clients = {}

      function getAllTestCases() {
        $http.get('/testcase/').success(function(data) {
          $scope.clients = data;
          $mdToast.show(
             $mdToast.simple()
               .textContent('Data table refreshed!')                       
               .hideDelay(3000)
           );
        });
      }
      getAllTestCases();
      
      setInterval(function() {
        getAllTestCases();
      }, 30000);

      $scope.refresh = function() {
        getAllTestCases();
      };

      $scope.saveTestCase = function() {
        $http({
           method: 'POST',
           url: '/testcase/',
           data: $.param($scope.project), // pass in data as strings
           headers: {
             'Content-Type': 'application/x-www-form-urlencoded'
           } // set the headers so angular passing info as form data (not request payload)*/
         })
         .success(function(data) {
           //debugger;
           console.log(data);
           $mdToast.show(
             $mdToast.simple()
               .textContent('Created Testcase successfully!')                       
               .hideDelay(3000)
           );
           $scope.projectForm.$setPristine();
           $scope.projectForm.$setUntouched();
           $scope.project = {};
           getAllTestCases();
         });
      };
    }