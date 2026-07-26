# Foundry Audit Workflow

## Invariant Testing (forge test)
```solidity
import {Test} from "forge-std/Test.sol";
import {StdInvariant} from "forge-std/StdInvariant.sol";

contract AuditInvariants is StdInvariant, Test {
    Token token;

    function setUp() public {
        token = new Token();
        targetContract(address(token));
    }

    function invariant_totalSupply_eq_balanceSum() public {
        assertEq(token.totalSupply(), balanceSum());
    }
}
```

## Differential Testing
```solidity
function test_transfer_against_reference(uint256 amount, address to) public {
    vm.assume(to != address(0));
    uint refResult = referenceToken.transfer(to, amount);
    uint implResult = implToken.transfer(to, amount);
    assertEq(refResult, implResult);
}
```

## Fuzz Parameters
```solidity
/// forge-config: default.fuzz.runs = 50000
function test_fuzz_deposit_withdraw(uint96 amount) public {
    // ...
}
```

## Stack Traces
```bash
forge test -vvvv  # Full traces on failure
forge test --match-contract AuditInvariants --fuzz-runs 100000
```

## Gas Snapshots
```bash
forge snapshot --match-contract GasTest
forge snapshot --diff .gas-snapshot  # Compare with last run
```
