var corthusModule = angular.module('corthus', []);

corthusModule.config(function ($routeProvider) {
    $routeProvider
        .when('/text/:name/:chapter', {
            templateUrl: 'templates/text.html',
            controller: TextCtrl
        })
        .otherwise({
            redirectTo: '/text/Jn/1'
        });
});

function TextCtrl($rootScope, $scope, $http, $routeParams) {

    $scope.name = $routeParams.name;
    $scope.chapter = $routeParams.chapter;
    $scope.path = $routeParams.name + '/' + $routeParams.chapter;

    $rootScope.currentTextName = $routeParams.name;

    $http.get('api/' + $scope.path).success(function (data) {
        _.each($scope.langs, function (settings, lang) {
            lang.available = false;
        });
        _.each(data.langs, function(lang) {
            if (!$scope.langs[lang]) {
                $scope.langs[lang] = {};
            }
            $scope.langs[lang].available = true;
        });
        $scope.rungs = data.rungs;
    });

    $http.get('api/' + $routeParams.name + '/index').success(function (data) {
        $scope.chapters = data;
    });

    // langs are in $rootScope, because we want to remember selected languages when navigating
    // to another text
    if (!$rootScope.langs) {
        // these are just defaults - other languages are hidden by default
        $rootScope.langs = {
            cu: { visible: true },
            el: { visible: true },
            en: { visible: true },
            la: { visible: true },
            pl: { visible: true },
        };
    }

    $scope.title = function () {
        return _.find($scope.links, { name: $routeParams.name }).title;
    };
}

function NavCtrl($scope, $http, $rootScope) {
    $http.get('index.json').success(function (data) {
        $rootScope.links = data;
    });
}
