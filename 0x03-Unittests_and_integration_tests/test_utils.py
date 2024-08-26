#!/usr/bin/env python3

"""Test module for github org client utilities"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import Mock, patch
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)

class TestAccessNestedMap(unittest.TestCase):
    """
        Test that the 'access_nested_map' function returns the expected output
        when given a map and a nested path.

        Args:
            map (dict): The input dictionary.
            path (tuple): The nested path to access within the dictionary.
            expected_output: The expected output when
            accessing the specified path.

        Returns:
            None: This method asserts the equality of
            the actual and expected outputs.

        Raises:
            AssertionError: If the actual output does not
            match the expected output.
    """
    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )

    def test_access_nested_map(self, map, path, expected_output):
        output = access_nested_map(map, path)
        self.assertEqual(output, expected_output)

    @parameterized.expand([({}, ("a",), "a"), ({"a": 1}, ("a", "b"), "b")])

    def test_access_nested_map_exception(self, map, path, wrong_output):

        """
                Test that the 'access_nested_map' function raises the correct exception
                when given a map and an invalid nested path.

                Args:
                    map (dict): The input dictionary.
                    path (tuple): The nested path to access within the dictionary.
                    wrong_output: The expected exception message.

                Returns:
                    None: This method asserts the correctness of the raised exception.

                Raises:
                    AssertionError: If the exception message does not
                    match the expected message.
                """
        with self.assertRaises(KeyError) as e:
            access_nested_map(map, path)
            self.assertEqual(wrong_output, str(e.exception))


class TestGetJson(unittest.TestCase):
    """
        Test case class for the 'get_json' function.

        This class includes test methods to validate the behavior of the
        'get_json' function, which is responsible for retrieving JSON from
        specified URLs. The tests cover different scenarios, ensuring the function
        correctly handles various input cases.
    """
    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )

    def test_get_json(self, test_url, test_payload):
        """
            Tests that 'get_json' method returns the expected result

            Args:
                test_url (str): mock url used to test method.
                test_payload (dict): a dictionary arg to test payload exec.
                wrong_output: The expected exception message.

            Returns:
                None: This method asserts the correctness of the raised exception.

            Raises:
                AssertionError: If the exception message does not
                match the expected message.
            
        """

        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch("requests.get", return_value=mock_response):
            response = get_json(test_url)
            self.assertEqual(response, test_payload)
            mock_response.json.assert_called_once()

    class TestMemoize(unittest.TestCase):
        """Test case class for memoize function 
            
            This method tests that when calling a_property twice,the correct result is returned 
            but a_method is only called once using assert_called_once.
        """

        def test_memoize(self):
            """
                Test the 'memoize' decorator functionality.

                This test method creates a test class with a memoized property and
                verifies that the underlying method is called only once, even when
                the property is accessed multiple times.

                Returns:
                    None: Asserts the behavior of the 'memoize' decorator.

                Raises:
                    AssertionError: If the expected behavior is not
                    observed during testing.
            """
            class TestClass:

                def a_method(self):
                    return 42

                @memoize
                def a_property(self):
                    return self.a_method()

            with patch.object(TestClass, "a_method", return_value=42) as mocked:
                spec = TestClass()
                spec.a_property
                spec.a_property
                mocked.asset_called_once()