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

//    $scope.langs = ['pl', 'cu', 'el', 'en', 'fr', 'la'];
    $scope.langs = ['ar', 'cu', 'el', 'en', 'fr', 'la', 'zh-Hans'];
}

function NavCtrl($scope, $http, $routeParams) {
    $scope.links = ['Mt/1', 'Mk/1', 'Lk/1', 'Jn/1'];
}
