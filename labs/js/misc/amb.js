function ambRunWorker(id, workers, func) {
    var choices = [];
    var index;

    function amb(values) {
        if (values.length == 0) {
            fail();
        }
        if (index == choices.length) {
            var start = Math.floor(id * values.length / workers);
            choices.push({i: start,
                          start: start,
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
            while ((choice = choices.pop())) {
                if (++choice.i == choice.count) {
                    choice.i = 0;
                }
                if (choice.i != choice.start) {
                    break;
                }
            }
            if (choice == undefined) {
                return undefined;
            }
            choices.push(choice);
        }
    }
}
