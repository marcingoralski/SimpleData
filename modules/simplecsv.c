#include <Python.h>

static PyObject* simplecsv_serialize(PyObject* self, PyObject* args);

static PyMethodDef simplecsvMethods[] = {
    {"serialize_c", simplecsv_serialize, METH_VARARGS, "Serialize data to CSV using heap memory."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef simplecsvmodule = {
    PyModuleDef_HEAD_INIT,
    "simplecsv",
    "A simple CSV module",
    -1,
    simplecsvMethods
};

PyMODINIT_FUNC PyInit_simplecsv(void) {
    return PyModule_Create(&simplecsvmodule);
}

static PyObject* simplecsv_serialize(PyObject* self, PyObject* args) {
    PyObject *input_dict, *values, *item;
    Py_ssize_t values_count, i;
    size_t total_length = 0, len;
    char *current_pos, *result_str;

    if (!PyArg_ParseTuple(args, "O", &input_dict)) {
        return NULL;
    }

    values = PyDict_Values(input_dict);
    if (!values) {
        return NULL;
    }

    values_count = PyList_Size(values);
    if (values_count < 0) {
        Py_DECREF(values);
        return NULL;
    }

    for (i = 0; i < values_count; i++) {
        item = PyList_GetItem(values, i);
        if (!item) {
            Py_DECREF(values);
            return NULL;
        }
        PyObject *str_item = PyObject_Str(item);
        if (!str_item) {
            Py_DECREF(values);
            return NULL;
        }
        total_length += PyUnicode_GET_LENGTH(str_item) + 1;
        Py_DECREF(str_item);
    }

    result_str = (char *)malloc(total_length + 1);
    if (!result_str) {
        Py_DECREF(values);
        return PyErr_NoMemory();
    }

    current_pos = result_str;
    for (i = 0; i < values_count; i++) {
        item = PyList_GetItem(values, i);
        PyObject *str_item = PyObject_Str(item);
        if (!str_item) {
            free(result_str);
            Py_DECREF(values);
            return NULL;
        }
        const char *temp = PyUnicode_AsUTF8(str_item);
        if (!temp) {
            Py_DECREF(str_item);
            free(result_str);
            Py_DECREF(values);
            return NULL;
        }
        len = strlen(temp);
        memcpy(current_pos, temp, len);
        current_pos += len;
        *current_pos++ = ',';
        Py_DECREF(str_item);
    }
    if (values_count > 0) {
        current_pos--;
    }
    *current_pos = '\0';

    Py_DECREF(values);

    PyObject *final_result = PyUnicode_FromString(result_str);
    free(result_str);
    return final_result;
}