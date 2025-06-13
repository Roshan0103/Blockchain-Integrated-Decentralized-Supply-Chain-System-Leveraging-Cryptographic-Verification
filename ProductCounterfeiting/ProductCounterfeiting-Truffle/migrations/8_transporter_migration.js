const Transporter = artifacts.require("TransporterContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(Transporter);
        };
        