#include <Python.h>

static PyObject* simplecsv_serialize_on_stack(PyObject* self, PyObject* args);
static PyObject* simplecsv_serialize_on_heap(PyObject* self, PyObject* args);
// static PyObject* simplecsv_deserialize(PyObject* self, PyObject* args);

static PyMethodDef simplecsvMethods[] = {
    {"serialize_on_stack", simplecsv_serialize_on_stack, METH_VARARGS, "Serialize data to CSV using stack memory."},
    {"serialize_on_heap", simplecsv_serialize_on_heap, METH_VARARGS, "Serialize data to CSV using heap memory."},
    // {"deserialize", simplecsv_deserialize, METH_VARARGS, "Deserialize CSV to data"},
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
    Py_Initialize();
    return PyModule_Create(&simplecsvmodule);
}

#define MAX_STACK_ARRAY_SIZE 250000
static PyObject* simplecsv_serialize_on_stack(PyObject* self, PyObject* args) {
    PyObject *input_dict, *values, *item;
    Py_ssize_t total_length = 0, values_count, i;
    char *current_pos, *result_str;
    size_t len;
    
    char *temp[MAX_STACK_ARRAY_SIZE];

    if (!PyArg_ParseTuple(args, "O", &input_dict)) {
        return NULL;
    }

    values = PyDict_Values(input_dict);
    values_count = PyList_Size(values);

    if (values_count > MAX_STACK_ARRAY_SIZE) {
        Py_DECREF(values);
        PyErr_SetString(PyExc_ValueError, "Too many items in the dictionary");
        return NULL;
    }

    for (i = 0; i < values_count; i++) {
        item = PyList_GetItem(values, i);
        PyObject *str_item = PyObject_Str(item);
        temp[i] = PyUnicode_AsUTF8(str_item);
        total_length += strlen(temp[i]) + 1; // +1 for comma
    }

    result_str = (char *)malloc(total_length);
    if (!result_str) {
        for (i = 0; i < values_count; i++) {
            free(temp[i]);
        }
        return PyErr_NoMemory();
    }

    current_pos = result_str;
    for (i = 0; i < values_count; i++) {
        len = strlen(temp[i]);
        memcpy(current_pos, temp[i], len);
        current_pos += len;
        *current_pos++ = ',';
    }
    if (values_count > 0) {
        current_pos--; // Remove the last comma
    }
    *current_pos = '\0';

    Py_DECREF(values);

    PyObject *final_result = PyUnicode_FromString(result_str);
    free(result_str);

    return final_result;
}


static PyObject* simplecsv_serialize_on_heap(PyObject* self, PyObject* args) {
    PyObject *input_dict, *values, *item;
    Py_ssize_t values_count, i;
    size_t total_length = 0, len;
    char *current_pos, *result_str;

    if (!PyArg_ParseTuple(args, "O", &input_dict)) {
        return NULL;
    }

    values = PyDict_Values(input_dict);
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
        total_length += PyUnicode_GET_LENGTH(str_item) + 1; // +1 for comma
        Py_DECREF(str_item);
    }

    result_str = (char *)malloc(total_length);
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
        char *temp = PyUnicode_AsUTF8(str_item);
        len = strlen(temp);
        memcpy(current_pos, temp, len);
        current_pos += len;
        *current_pos++ = ',';
        Py_DECREF(str_item);
    }
    if (values_count > 0) {
        current_pos--; // Remove the last comma
    }
    *current_pos = '\0';

    Py_DECREF(values);

    PyObject *final_result = PyUnicode_FromString(result_str);
    free(result_str);
    return final_result;
}

