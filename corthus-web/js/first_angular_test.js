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

function TextCtrl($scope, $http, $routeParams) {

//    $scope.path = 'texts/kanon_izr.pt2';
//    $scope.path = 'gen/Jn/1';
    $scope.name = $routeParams.name;
    $scope.chapter = $routeParams.chapter;
    $scope.path = $routeParams.name + '/' + $routeParams.chapter;

    $http.get('api/' + $scope.path, {
        transformResponse: function (data) {
            // parsing PT into Javascript object.
            return _.map(data.split('\n\n'), function (rungStr) {
                var rungObj = {};
                _.forEach(rungStr.split('\n'), function (line) {
                    if (!line) {
                        return;
                    }
                    var match = line.match(/^([a-zA-Z-]+) (.*)$/); // line format
                    if (!match) {
                        console.error("parse error: line does not match: ", line);
                        return;
                    }
                    var list = rungObj[match[1]] || [];
                    list.push(match[2]);
                    rungObj[match[1]] = list;
                });
                return rungObj;
            });
        }
    }).success(function (data) {
            $scope.rungs = data;
        });

    $http.get('api/' + $routeParams.name + '/index').success(function (data) {
            $scope.chapters = data;
        });

    $scope.langs = [/* 'pl', */ 'ar', 'cu', 'el', 'en', 'fr', 'la', 'zh-Hans'];

    $scope.title = function () {
        return _.find($scope.links, { name: $scope.name }).title;
    };
}

function NavCtrl($scope, $http, $rootScope) {
    $http.get('index.json').success(function (data) {
        $rootScope.links = data;
        console.log(data);
    });
}
