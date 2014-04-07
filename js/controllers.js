.controller("LoginController", ["$scope", "$firebase", "$firebaseSimpleLogin",
  function($scope, $firebase, $firebaseSimpleLogin) {
    var ref = new Firebase("https://junkiatyeo.firebaseio.com");
    $scope.auth = $firebaseSimpleLogin(ref);
  }
])
.controller("SimpleAccessController", ["$rootScope", "$scope",
  function($rootScope, $scope) {
    $rootScope.$on("$firebaseSimpleLogin:login", function(e, user) {
      console.log("SimpleAccess");
      $scope.uid = user.uid;
    });

    $rootScope.$on("$firebaseSimpleLogin:logout", function(e, user) {
      $scope.uid = null;
    });
  }
])