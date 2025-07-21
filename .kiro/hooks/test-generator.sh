#!/bin/bash

# Kiro AI IDE - Automated Test Generation Hook
# Generates appropriate tests for new code files

set -euo pipefail

SOURCE_FILE="$1"
TEST_TYPE="${2:-unit}"

echo "🧪 Generating tests for: $SOURCE_FILE"

# Determine test file path and framework
get_test_info() {
    local source_file="$1"
    local dir_name=$(dirname "$source_file")
    local base_name=$(basename "$source_file" | sed 's/\.[^.]*$//')
    local extension="${source_file##*.}"
    
    case "$extension" in
        js|ts)
            echo "javascript" "$dir_name/__tests__/$base_name.test.ts" "jest"
            ;;
        tsx)
            echo "react" "$dir_name/__tests__/$base_name.test.tsx" "jest"
            ;;
        py)
            echo "python" "tests/test_$base_name.py" "pytest"
            ;;
        go)
            echo "go" "${base_name}_test.go" "go-test"
            ;;
        *)
            echo "generic" "tests/$base_name.test" "generic"
            ;;
    esac
}

read -r LANGUAGE TEST_FILE FRAMEWORK <<< "$(get_test_info "$SOURCE_FILE")"

# Generate test template based on language
generate_javascript_test() {
    local source_file="$1"
    local test_file="$2"
    local module_name=$(basename "$source_file" | sed 's/\.[^.]*$//')
    
    mkdir -p "$(dirname "$test_file")"
    
    cat > "$test_file" << EOF
import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { ${module_name} } from '../${module_name}';

describe('${module_name}', () => {
  beforeEach(() => {
    // Setup test environment
  });

  afterEach(() => {
    // Cleanup test environment
  });

  describe('when initialised', () => {
    it('should have expected default state', () => {
      // Arrange
      
      // Act
      
      // Assert
      expect(true).toBe(true); // Replace with actual test
    });
  });

  describe('when processing valid input', () => {
    it('should return expected output', () => {
      // Arrange
      const input = {};
      const expected = {};
      
      // Act
      const result = ${module_name}(input);
      
      // Assert
      expect(result).toEqual(expected);
    });
  });

  describe('when processing invalid input', () => {
    it('should handle errors gracefully', () => {
      // Arrange
      const invalidInput = null;
      
      // Act & Assert
      expect(() => ${module_name}(invalidInput)).toThrow();
    });
  });

  describe('edge cases', () => {
    it('should handle empty input', () => {
      // Arrange
      const emptyInput = {};
      
      // Act
      const result = ${module_name}(emptyInput);
      
      // Assert
      expect(result).toBeDefined();
    });

    it('should handle large input sets', () => {
      // Arrange
      const largeInput = Array(1000).fill({}).map((_, i) => ({ id: i }));
      
      // Act
      const result = ${module_name}(largeInput);
      
      // Assert
      expect(result).toBeDefined();
    });
  });
});
EOF

    echo "📝 Generated JavaScript/TypeScript test: $test_file"
}

generate_python_test() {
    local source_file="$1"
    local test_file="$2"
    local module_name=$(basename "$source_file" | sed 's/\.[^.]*$//')
    
    mkdir -p "$(dirname "$test_file")"
    
    cat > "$test_file" << EOF
"""Tests for ${module_name} module."""

import pytest
from unittest.mock import Mock, patch
from src.${module_name} import ${module_name}


class Test${module_name^}:
    """Test suite for ${module_name} functionality."""

    def setup_method(self):
        """Set up test environment before each test."""
        pass

    def teardown_method(self):
        """Clean up test environment after each test."""
        pass

    def test_should_have_expected_default_state_when_initialised(self):
        """Test that ${module_name} has correct initial state."""
        # Arrange
        
        # Act
        result = ${module_name}()
        
        # Assert
        assert result is not None

    def test_should_return_expected_output_when_processing_valid_input(self):
        """Test that ${module_name} processes valid input correctly."""
        # Arrange
        valid_input = {}
        expected = {}
        
        # Act
        result = ${module_name}(valid_input)
        
        # Assert
        assert result == expected

    def test_should_handle_errors_gracefully_when_processing_invalid_input(self):
        """Test that ${module_name} handles invalid input appropriately."""
        # Arrange
        invalid_input = None
        
        # Act & Assert
        with pytest.raises(ValueError):
            ${module_name}(invalid_input)

    def test_should_handle_empty_input(self):
        """Test edge case with empty input."""
        # Arrange
        empty_input = {}
        
        # Act
        result = ${module_name}(empty_input)
        
        # Assert
        assert result is not None

    def test_should_handle_large_input_sets(self):
        """Test performance with large input sets."""
        # Arrange
        large_input = [{"id": i} for i in range(1000)]
        
        # Act
        result = ${module_name}(large_input)
        
        # Assert
        assert result is not None

    @patch('src.${module_name}.external_dependency')
    def test_should_handle_external_dependency_failure(self, mock_dependency):
        """Test error handling for external dependencies."""
        # Arrange
        mock_dependency.side_effect = Exception("External service unavailable")
        
        # Act & Assert
        with pytest.raises(Exception):
            ${module_name}({})


# Integration tests
class Test${module_name^}Integration:
    """Integration tests for ${module_name}."""

    def test_should_integrate_with_other_modules(self):
        """Test integration with other system components."""
        # Arrange
        
        # Act
        
        # Assert
        assert True  # Replace with actual integration test


# Property-based tests
class Test${module_name^}Properties:
    """Property-based tests for ${module_name}."""

    @pytest.mark.parametrize("input_value", [
        {},
        {"key": "value"},
        {"multiple": "keys", "with": "values"},
    ])
    def test_should_handle_various_input_formats(self, input_value):
        """Test ${module_name} with various input formats."""
        # Act
        result = ${module_name}(input_value)
        
        # Assert
        assert result is not None
EOF

    echo "📝 Generated Python test: $test_file"
}

generate_go_test() {
    local source_file="$1"
    local test_file="$2"
    local package_name=$(dirname "$source_file" | xargs basename)
    
    cat > "$test_file" << EOF
package ${package_name}

import (
    "context"
    "testing"
    "time"
)

func TestShouldHaveExpectedDefaultStateWhenInitialised(t *testing.T) {
    // Arrange
    
    // Act
    
    // Assert
    if true != true { // Replace with actual test
        t.Errorf("Expected true, got false")
    }
}

func TestShouldReturnExpectedOutputWhenProcessingValidInput(t *testing.T) {
    // Arrange
    ctx := context.Background()
    input := struct{}{}
    
    // Act
    result, err := ProcessData(ctx, input)
    
    // Assert
    if err != nil {
        t.Errorf("Expected no error, got %v", err)
    }
    
    if result == nil {
        t.Error("Expected result, got nil")
    }
}

func TestShouldHandleErrorsGracefullyWhenProcessingInvalidInput(t *testing.T) {
    // Arrange
    ctx := context.Background()
    invalidInput := struct{}{}
    
    // Act
    _, err := ProcessData(ctx, invalidInput)
    
    // Assert
    if err == nil {
        t.Error("Expected error for invalid input, got nil")
    }
}

func TestShouldHandleContextCancellation(t *testing.T) {
    // Arrange
    ctx, cancel := context.WithCancel(context.Background())
    cancel() // Cancel immediately
    
    // Act
    _, err := ProcessData(ctx, struct{}{})
    
    // Assert
    if err == nil {
        t.Error("Expected context cancellation error, got nil")
    }
}

func TestShouldHandleTimeout(t *testing.T) {
    // Arrange
    ctx, cancel := context.WithTimeout(context.Background(), 1*time.Millisecond)
    defer cancel()
    
    // Act
    _, err := ProcessData(ctx, struct{}{})
    
    // Assert
    if err == nil {
        t.Error("Expected timeout error, got nil")
    }
}

// Benchmark tests
func BenchmarkProcessData(b *testing.B) {
    ctx := context.Background()
    input := struct{}{}
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        ProcessData(ctx, input)
    }
}

// Table-driven tests
func TestProcessDataVariousInputs(t *testing.T) {
    testCases := []struct {
        name        string
        input       interface{}
        expectError bool
    }{
        {"valid input", struct{}{}, false},
        {"nil input", nil, true},
        {"empty input", struct{}{}, false},
    }
    
    for _, tc := range testCases {
        t.Run(tc.name, func(t *testing.T) {
            ctx := context.Background()
            _, err := ProcessData(ctx, tc.input)
            
            if tc.expectError && err == nil {
                t.Errorf("Expected error for %s, got nil", tc.name)
            }
            
            if !tc.expectError && err != nil {
                t.Errorf("Expected no error for %s, got %v", tc.name, err)
            }
        })
    }
}
EOF

    echo "📝 Generated Go test: $test_file"
}

# Main test generation logic
main() {
    if [[ ! -f "$SOURCE_FILE" ]]; then
        echo "❌ Error: Source file not found: $SOURCE_FILE"
        exit 1
    fi
    
    echo "🎯 Test Generation Summary:"
    echo "  Source: $SOURCE_FILE"
    echo "  Language: $LANGUAGE"
    echo "  Framework: $FRAMEWORK"
    echo "  Test File: $TEST_FILE"
    echo ""
    
    case "$LANGUAGE" in
        "javascript"|"react")
            generate_javascript_test "$SOURCE_FILE" "$TEST_FILE"
            ;;
        "python")
            generate_python_test "$SOURCE_FILE" "$TEST_FILE"
            ;;
        "go")
            generate_go_test "$SOURCE_FILE" "$TEST_FILE"
            ;;
        *)
            echo "⚠️  Generic test template not implemented for $LANGUAGE"
            echo "📝 Create test file manually at: $TEST_FILE"
            ;;
    esac
    
    echo ""
    echo "✅ Test generation complete!"
    echo "💡 Remember to:"
    echo "   • Update test cases with actual business logic"
    echo "   • Add integration tests if needed"
    echo "   • Run tests to ensure they pass"
    echo "   • Achieve target test coverage (90%+)"
}

main "$@"