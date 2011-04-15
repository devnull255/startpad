function ambRun(func) {
    var choices = [];
    var index;

    function amb(values) {
        if (values.length == 0) {
            fail();
        }
        if (index == choices.length) {
            choices.push({i: 0,
                          count: values.length});
        }
        var choice = choices[index++];
        return values[choice.i];
    }

    function fail() { throw fail; }

    while (true) {
        try {
            index = 0;
            return func(amb, fail);
        } catch (e) {
            if (e != fail) {
                throw e;
            }
            var choice;
            while ((choice = choices.pop()) && ++choice.i == choice.count) {}
            if (choice == undefined) {
                return undefined;
            }
            choices.push(choice);
        }
    }
}