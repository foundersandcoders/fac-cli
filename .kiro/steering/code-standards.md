# Code Generation Standards

## Overview
These standards guide all code generation and modification activities within the Kiro AI IDE environment.

## General Principles

### Code Quality
- **Functional First**: Prefer functional programming patterns over object-oriented
- **Pure Functions**: Functions should be side-effect free when possible
- **Immutability**: Use immutable data structures by default
- **Single Responsibility**: Each function/module serves one clear purpose
- **Explicit over Implicit**: Code should be self-documenting

### Naming Conventions
- **Functions**: `camelCase` (JS/TS), `snake_case` (Python), `camelCase` (Go)
- **Constants**: `UPPER_SNAKE_CASE`
- **Types/Classes**: `PascalCase`
- **Files**: `kebab-case` for multi-word names
- **Directories**: `kebab-case` for multi-word names

## Language-Specific Standards

### JavaScript/TypeScript
```typescript
// Prefer const over let, never use var
const processData = (input: InputType): OutputType => {
  // Use early returns to reduce nesting
  if (!input.isValid) {
    return createError('Invalid input');
  }
  
  // Use destructuring for cleaner code
  const { id, name, metadata } = input;
  
  // Use array methods over loops
  return input.items
    .filter(item => item.active)
    .map(item => transformItem(item));
};

// Type everything explicitly
interface ProcessOptions {
  readonly validateInput: boolean;
  readonly includeMetadata: boolean;
}

// Use readonly for immutability
type ProcessResult = readonly [
  data: ProcessedData,
  metadata: Metadata
];
```

### Python
```python
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from functools import partial

# Use dataclasses for simple data containers
@dataclass(frozen=True)  # frozen=True for immutability
class ProcessOptions:
    validate_input: bool
    include_metadata: bool

def process_data(
    input_data: Dict[str, Union[str, int]], 
    options: ProcessOptions
) -> Optional[List[Dict[str, str]]]:
    """Process input data according to specified options.
    
    Args:
        input_data: The data to process
        options: Processing configuration
        
    Returns:
        Processed data or None if invalid
    """
    # Use early returns
    if not options.validate_input or not _is_valid(input_data):
        return None
    
    # Use list comprehensions over loops
    return [
        _transform_item(item) 
        for item in input_data.get('items', [])
        if item.get('active', False)
    ]

def _is_valid(data: Dict[str, Union[str, int]]) -> bool:
    """Private helper function for validation."""
    return bool(data and 'items' in data)
```

### Go
```go
package main

import (
    "context"
    "fmt"
)

// Use interfaces for dependency injection
type DataProcessor interface {
    ProcessData(ctx context.Context, input ProcessInput) (ProcessOutput, error)
}

// Use struct embedding for composition
type ProcessInput struct {
    ID       string            `json:"id"`
    Items    []ProcessItem     `json:"items"`
    Metadata map[string]string `json:"metadata"`
}

type ProcessOutput struct {
    Results []ProcessResult `json:"results"`
    Count   int            `json:"count"`
}

// Methods on structs for domain logic
func (p ProcessInput) Validate() error {
    if p.ID == "" {
        return fmt.Errorf("id is required")
    }
    if len(p.Items) == 0 {
        return fmt.Errorf("items cannot be empty")
    }
    return nil
}

// Use context for cancellation and timeouts
func ProcessData(ctx context.Context, input ProcessInput) (ProcessOutput, error) {
    if err := input.Validate(); err != nil {
        return ProcessOutput{}, fmt.Errorf("validation failed: %w", err)
    }
    
    var results []ProcessResult
    for _, item := range input.Items {
        if !item.Active {
            continue
        }
        
        result, err := processItem(ctx, item)
        if err != nil {
            return ProcessOutput{}, fmt.Errorf("processing item %s: %w", item.ID, err)
        }
        
        results = append(results, result)
    }
    
    return ProcessOutput{
        Results: results,
        Count:   len(results),
    }, nil
}
```

## Testing Standards

### Test Structure
```
// Arrange - Set up test data and conditions
// Act - Execute the code under test
// Assert - Verify the results
```

### Test Naming
- Test functions: `test_should_return_error_when_input_invalid`
- Test descriptions should be readable sentences

### Test Coverage
- Aim for 90%+ coverage
- Test edge cases and error conditions
- Use mocks for external dependencies

## Error Handling Standards

### Error Types
- **Validation Errors**: Input doesn't meet requirements
- **Business Logic Errors**: Domain rules violated
- **System Errors**: Infrastructure failures
- **Not Found Errors**: Requested resource doesn't exist

### Error Messages
- Include context about what went wrong
- Suggest corrective action when possible
- Never expose sensitive information
- Use consistent error codes/types

## Documentation Standards

### Inline Comments
- Explain WHY not WHAT
- Document complex algorithms
- Note important assumptions
- Explain non-obvious code

### API Documentation
- Document all public functions/methods
- Include parameter descriptions
- Provide usage examples
- Document error conditions

## Performance Guidelines

### General Rules
- Profile before optimising
- Optimise for readability first, performance second
- Cache expensive computations
- Use appropriate data structures

### Memory Management
- Avoid memory leaks
- Clean up resources (files, connections)
- Use object pools for frequently allocated objects
- Monitor memory usage in tests

## Security Guidelines

### Input Validation
- Validate all inputs at boundaries
- Sanitise data before processing
- Use allowlists over denylists
- Never trust user input

### Data Protection
- No secrets in code or logs
- Encrypt sensitive data at rest
- Use HTTPS for all network communication
- Implement proper authentication

---

*These standards should be applied to all code generation and modification activities. They will be enforced by agent hooks and code review processes.*