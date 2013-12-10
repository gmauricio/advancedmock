from mock import MagicMock

class AdvancedMagicMock(MagicMock):
    def assert_called_with(self, *args, **kwargs):
        """assert that the mock was called with the specified arguments.

        Raises an AssertionError if the args and keyword args passed in are
        different to the last call to the mock."""

        if self.call_args is None:
            expected = self._format_mock_call_signature(args, kwargs)
            raise AssertionError('Expected call: %s\nNot called' % (expected,))

        self._assert_with_constraints(args, kwargs, self.call_args)

    def assert_any_call(self, *args, **kwargs):
        """assert the mock has been called with the specified arguments.

        The assert passes if the mock has *ever* been called, unlike
        `assert_called_with` and `assert_called_once_with` that only pass if
        the call is the most recent one."""
        at_least_on_passed = False
        for kall in self.call_args_list:
            try:
                self._assert_with_constraints(args, kwargs, kall)
                #assertions passed, return because there's a match
                return
            except AssertionError:
                #keep trying
                pass

        expected_string = self._format_mock_call_signature(args, kwargs)
        raise AssertionError(
            '%s call not found' % expected_string
        )

    def _assert_with_constraints(self, args, kwargs, kall):
        call_args = kall[0]
        #call_kwargs = kall[1] TODO: check kwargs as well!
        for idx, arg in enumerate(args):
            self._assert_with_constraint(arg, call_args[idx], args, kwargs)

    def _assert_with_constraint(self, arg, call_arg, args, kwargs):
        if isinstance(arg, Constraint):
            if not arg.check(call_arg):
                msg = self._format_mock_failure_message(args, kwargs)
                raise AssertionError(msg)
        else:
            if not arg == call_arg:
                msg = self._format_mock_failure_message(args, kwargs)
                raise AssertionError(msg)


class Constraint():
    def check(self, value):
        return True


class InstanceOf(Constraint):
    def __init__(self, instance_type):
        self.instance_type = instance_type

    def check(self, value):
        return isinstance(value, self.instance_type)


class StringOfLen(Constraint):
    def __init__(self, expected_len):
        self.expected_len = expected_len

    def check(self, value):
        return len(value) == self.expected_len


class NonEmptyString(Constraint):
    def check(self, value):
        return len(value) > 0


class ObjectThatCompliesWith(Constraint):
    def __init__(self, check_function, args=None):
        self.check_function = check_function
        self.args = args

    def check(self, value):
        return self.check_function(value, self.args)

