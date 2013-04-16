function TextCtrl($scope, $http) {

//    var path = 'texts/kanon_izr.pt2';
    $scope.path = 'gen/Jn/1';

    $http.get($scope.path, {
        transformResponse: function (data) {
            // parsing PT into Javascript object.
            return _.map(data.split('\n\n'), function (rungStr) {
                var rungObj = {};
                _.forEach(rungStr.split('\n'), function (line) {
                    if (!line) {
                        return;
                    }
                    var match = line.match(/^([a-z]+) (.*)$/); // line format
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

    $scope.langs = ['pl', 'cu', 'el', 'en', 'fr', 'la'];
}