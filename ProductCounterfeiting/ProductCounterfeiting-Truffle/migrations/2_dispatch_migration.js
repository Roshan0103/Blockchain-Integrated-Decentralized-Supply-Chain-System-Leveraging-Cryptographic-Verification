const Dispatch = artifacts.require("DispatchContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(Dispatch);
        };
        