import pytest

from components.parameter import IntegerParameter, FloatParameter, BooleanParameter, Parameter


class TestParameters:

    def test_create_parameters(self):
        make_int_param = Parameter(1, 0, 10)
        make_int_value_param = Parameter(1)
        make_float_param = Parameter(1.0, 0.0, 10.0)
        make_bool_param = Parameter(True)
        assert isinstance(make_int_param.value, IntegerParameter)
        assert isinstance(make_int_value_param.value, IntegerParameter)
        assert isinstance(make_float_param.value, FloatParameter)
        assert isinstance(make_bool_param.value, BooleanParameter)

    def test_initialize_parameters(self):
        int_param = IntegerParameter(1, 0, 10)
        float_param = FloatParameter(1.0, 0.0, 10.0)
        bool_param = BooleanParameter(True)
        assert int_param.value == 1
        assert int_param.min_value == 0
        assert int_param.max_value == 10
        assert float_param.value == 1.0
        assert float_param.min_value == 0.0
        assert float_param.max_value == 10.0
        assert bool_param.value == True

        with pytest.raises(ValueError):
            bad_int_param = IntegerParameter(11, 0, 10)
            bad_float_param = FloatParameter(11.0, 0.0, 10.0)
            bad_bool_param = BooleanParameter(1)


    def test_params_str(self):
        int_param = IntegerParameter(1, 0, 10)
        bool_param = BooleanParameter(True)
        assert str(int_param) == '1 (min_value=0, max_value=10)'
        assert str(bool_param) == 'True'


