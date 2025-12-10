import unittest
import sys

def run_all_tests():
    """Запускает все тесты"""
    loader = unittest.TestLoader()
    
    suite = loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_all_tests())